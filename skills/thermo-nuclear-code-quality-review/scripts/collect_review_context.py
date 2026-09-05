#!/usr/bin/env python3
"""Collect bounded, read-only Git metadata for a structural code review."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


def git(repo: Path, *args: str, check: bool = True) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), "-c", "core.quotepath=false", *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if check and result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {detail}")
    return result.stdout.rstrip("\n")


def ref_exists(repo: Path, ref: str) -> bool:
    return subprocess.run(
        ["git", "-C", str(repo), "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode == 0


def resolve_base(repo: Path, requested: str | None) -> tuple[str | None, str]:
    if requested:
        if not ref_exists(repo, requested):
            raise RuntimeError(f"requested base does not resolve to a commit: {requested}")
        return requested, "requested"

    remote_head = git(
        repo,
        "symbolic-ref",
        "--quiet",
        "--short",
        "refs/remotes/origin/HEAD",
        check=False,
    ).strip()
    candidates = [remote_head, "origin/main", "main", "origin/master", "master"]
    for candidate in dict.fromkeys(item for item in candidates if item):
        if ref_exists(repo, candidate):
            return candidate, "inferred"
    return None, "unresolved"


def parse_name_status(raw: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    parts = [part for part in raw.split("\0") if part]
    for index in range(0, len(parts), 2):
        if index + 1 < len(parts):
            entries.append({"status": parts[index], "path": parts[index + 1]})
    return entries


def parse_numstat(raw: str) -> dict[str, dict[str, int | None]]:
    result: dict[str, dict[str, int | None]] = {}
    for record in raw.split("\0"):
        parts = record.split("\t", 2)
        if len(parts) != 3:
            continue
        additions = None if parts[0] == "-" else int(parts[0])
        deletions = None if parts[1] == "-" else int(parts[1])
        result[parts[2]] = {"additions": additions, "deletions": deletions}
    return result


def diff_scope(repo: Path, *prefix: str) -> dict[str, Any]:
    common = [*prefix, "--no-renames"]
    return {
        "name_status": parse_name_status(git(repo, "diff", *common, "--name-status", "-z")),
        "numstat": parse_numstat(git(repo, "diff", *common, "--numstat", "-z")),
    }


def line_count(path: Path, max_file_bytes: int) -> tuple[int | None, bool, str | None]:
    if not path.is_file():
        return None, False, None
    if path.stat().st_size > max_file_bytes:
        return None, False, "size_limit"
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None, True, "binary"
    count = data.count(b"\n")
    if data and not data.endswith(b"\n"):
        count += 1
    return count, False, None


def applicable_instruction_files(repo: Path, paths: list[str]) -> list[str]:
    names = ("AGENTS.md", "agents.md", "CLAUDE.md")
    found: set[str] = set()

    for name in names:
        candidate = repo / name
        if candidate.is_file():
            found.add(candidate.relative_to(repo).as_posix())

    for raw_path in paths:
        current = (repo / raw_path).parent
        while current != repo and repo in current.parents:
            for name in names:
                candidate = current / name
                if candidate.is_file():
                    found.add(candidate.relative_to(repo).as_posix())
            current = current.parent

    github_instructions = repo / ".github" / "copilot-instructions.md"
    if github_instructions.is_file():
        found.add(github_instructions.relative_to(repo).as_posix())
    return sorted(found)


def build_context(args: argparse.Namespace) -> dict[str, Any]:
    if args.line_threshold <= 0 or args.max_file_bytes <= 0:
        raise RuntimeError("--line-threshold and --max-file-bytes must be positive")
    if args.max_untracked < 0 or args.max_files < 0:
        raise RuntimeError("--max-untracked and --max-files cannot be negative")

    requested_repo = Path(args.repo).expanduser().resolve()
    repo = Path(git(requested_repo, "rev-parse", "--show-toplevel")).resolve()
    base_ref, base_source = resolve_base(repo, args.base)
    head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "branch", "--show-current") or None

    scopes: dict[str, dict[str, Any]] = {}
    merge_base: str | None = None
    if base_ref:
        merge_base = git(repo, "merge-base", base_ref, "HEAD")
        scopes["branch"] = {
            "range": f"{merge_base}..HEAD",
            **diff_scope(repo, f"{merge_base}..HEAD"),
        }
    else:
        scopes["branch"] = {"range": None, "name_status": [], "numstat": {}}

    scopes["staged"] = {"range": "HEAD..index", **diff_scope(repo, "--cached")}
    scopes["unstaged"] = {"range": "index..worktree", **diff_scope(repo)}

    all_untracked = [
        path
        for path in git(repo, "ls-files", "--others", "--exclude-standard", "-z").split("\0")
        if path
    ]
    untracked = all_untracked[: args.max_untracked]
    scopes["untracked"] = {
        "range": "untracked",
        "name_status": [{"status": "?", "path": path} for path in untracked],
        "numstat": {},
        "total": len(all_untracked),
        "truncated": len(untracked) < len(all_untracked),
    }

    for path in untracked:
        lines, binary, _ = line_count(repo / path, args.max_file_bytes)
        scopes["untracked"]["numstat"][path] = {
            "additions": None if binary else lines,
            "deletions": 0,
        }

    ordered_paths: list[str] = []
    seen_paths: set[str] = set()
    for scope_name in ("staged", "unstaged", "untracked", "branch"):
        for entry in scopes[scope_name]["name_status"]:
            path = entry["path"]
            if path not in seen_paths:
                seen_paths.add(path)
                ordered_paths.append(path)

    selected_paths = set(ordered_paths[: args.max_files])
    changed_file_total = len(ordered_paths)
    for scope in scopes.values():
        scope_total = len(scope["name_status"])
        scope["name_status"] = [
            entry for entry in scope["name_status"] if entry["path"] in selected_paths
        ]
        scope["numstat"] = {
            path: delta for path, delta in scope["numstat"].items() if path in selected_paths
        }
        scope["total_files"] = scope_total
        scope["file_details_truncated"] = len(scope["name_status"]) < scope_total

    files: dict[str, dict[str, Any]] = {}
    for scope_name, scope in scopes.items():
        for entry in scope["name_status"]:
            path = entry["path"]
            record = files.setdefault(path, {"path": path, "scopes": [], "statuses": {}})
            record["scopes"].append(scope_name)
            record["statuses"][scope_name] = entry["status"]
        for path, delta in scope["numstat"].items():
            record = files.setdefault(path, {"path": path, "scopes": [], "statuses": {}})
            record.setdefault("deltas", {})[scope_name] = delta

    threshold_crossings: list[str] = []
    for path, record in files.items():
        current_lines, binary, skipped_reason = line_count(repo / path, args.max_file_bytes)
        record["exists"] = (repo / path).exists()
        record["binary"] = binary
        record["current_lines"] = current_lines
        if skipped_reason:
            record["line_count_skipped"] = skipped_reason
        record["scopes"] = sorted(set(record["scopes"]))

        deltas = record.get("deltas", {})
        numeric_deltas = [
            delta
            for delta in deltas.values()
            if delta.get("additions") is not None and delta.get("deletions") is not None
        ]
        if current_lines is not None and numeric_deltas:
            net = sum(int(delta["additions"]) - int(delta["deletions"]) for delta in numeric_deltas)
            baseline_estimate = current_lines - net
            record["baseline_line_estimate"] = baseline_estimate
            crosses = baseline_estimate < args.line_threshold <= current_lines
            record["crosses_line_threshold"] = crosses
            if crosses:
                threshold_crossings.append(path)

    changed_paths = sorted(files)
    return {
        "schema_version": 1,
        "repository": str(repo),
        "branch": branch,
        "head": head,
        "base": {"ref": base_ref, "source": base_source, "merge_base": merge_base},
        "line_threshold": args.line_threshold,
        "changed_file_total": changed_file_total,
        "file_records_returned": len(changed_paths),
        "max_files": args.max_files,
        "tracked_status_porcelain_v2": git(
            repo, "status", "--porcelain=v2", "--branch", "--untracked-files=no"
        ).splitlines(),
        "applicable_instruction_files": applicable_instruction_files(repo, changed_paths),
        "scopes": scopes,
        "files": [files[path] for path in changed_paths],
        "threshold_crossings": threshold_crossings,
        "warnings": [
            message
            for condition, message in (
                (base_source == "inferred", f"base was inferred as {base_ref}"),
                (base_source == "unresolved", "branch base could not be resolved"),
                (scopes["untracked"]["truncated"], "untracked file list was truncated"),
                (
                    len(changed_paths) < changed_file_total,
                    f"changed file details were truncated to {len(changed_paths)} of {changed_file_total}; narrow the review or raise --max-files",
                ),
            )
            if condition
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Path inside the Git repository")
    parser.add_argument("--base", help="Base ref for committed branch changes")
    parser.add_argument("--line-threshold", type=int, default=1000)
    parser.add_argument("--max-untracked", type=int, default=500)
    parser.add_argument("--max-file-bytes", type=int, default=5_000_000)
    parser.add_argument("--max-files", type=int, default=2000)
    parser.add_argument("--pretty", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        context = build_context(args)
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"collect_review_context: {error}", file=sys.stderr)
        return 2
    print(json.dumps(context, indent=2 if args.pretty else None, sort_keys=args.pretty))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

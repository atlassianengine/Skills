#!/usr/bin/env python3
"""Emit bounded heuristic signals for behavior-preserving refactor triage.

Confidence describes pattern-match confidence, not impact or refactor priority.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from dataclasses import asdict
from pathlib import Path
from typing import Iterable

from smell_scan_rules import Signal, scan_source, signal_sort_key


DEFAULT_EXTENSIONS = {
    ".astro",
    ".js",
    ".jsx",
    ".py",
    ".rs",
    ".svelte",
    ".ts",
    ".tsx",
}
IGNORE_DIRS = {
    ".git",
    ".next",
    ".turbo",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
}


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_files(root: Path, extensions: set[str]) -> Iterable[Path]:
    if root.is_file():
        if root.suffix.lower() in extensions:
            yield root
        return

    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            relative_parts = path.relative_to(root).parts
        except ValueError:
            relative_parts = path.parts
        if any(part in IGNORE_DIRS for part in relative_parts):
            continue
        if path.suffix.lower() in extensions:
            yield path


def collect_files(roots: list[Path], extensions: set[str]) -> tuple[list[Path], list[str]]:
    files: dict[Path, None] = {}
    warnings: list[str] = []
    for root in roots:
        if not root.exists():
            warnings.append(f"missing path: {root}")
            continue
        for path in iter_files(root, extensions):
            files[path.resolve()] = None
    return sorted(files), warnings


def read_source(path: Path, max_file_bytes: int) -> tuple[str | None, str | None]:
    size = path.stat().st_size
    if size > max_file_bytes:
        return None, f"size limit ({size} > {max_file_bytes} bytes)"
    data = path.read_bytes()
    if b"\0" in data[:8192]:
        return None, "binary content"
    try:
        return data.decode("utf-8"), None
    except UnicodeDecodeError:
        return data.decode("utf-8", errors="replace"), "invalid UTF-8 replaced"


def validate_limits(args: argparse.Namespace) -> None:
    if args.max_files < 0 or args.max_findings < 0:
        raise ValueError("--max-files and --max-findings cannot be negative")
    if min(
        args.max_file_bytes,
        args.line_threshold,
        args.function_threshold,
        args.decision_threshold,
    ) <= 0:
        raise ValueError("size and threshold arguments must be positive")


def build_report(args: argparse.Namespace) -> dict[str, object]:
    validate_limits(args)
    cwd = Path.cwd().resolve()
    roots = [Path(value).expanduser().resolve() for value in args.paths]
    extensions = {
        value if value.startswith(".") else f".{value}"
        for value in (part.strip().lower() for part in args.extensions.split(","))
        if value
    }
    discovered, warnings = collect_files(roots, extensions)
    selected = discovered[: args.max_files]
    if len(selected) < len(discovered):
        warnings.append(
            f"file details truncated to {len(selected)} of {len(discovered)}; narrow paths or raise --max-files"
        )

    signals: list[Signal] = []
    skipped: list[dict[str, str]] = []
    scanned_count = 0
    for path in selected:
        text, read_warning = read_source(path, args.max_file_bytes)
        shown_path = display_path(path, cwd)
        if text is None:
            skipped.append({"path": shown_path, "reason": read_warning or "unreadable"})
            continue
        if read_warning:
            warnings.append(f"{shown_path}: {read_warning}")
        scanned_count += 1
        file_signals, file_warnings = scan_source(
            path=path,
            shown_path=shown_path,
            text=text,
            line_threshold=args.line_threshold,
            function_threshold=args.function_threshold,
            decision_threshold=args.decision_threshold,
        )
        signals.extend(file_signals)
        warnings.extend(file_warnings)

    unique_signals = sorted(set(signals), key=signal_sort_key)
    signal_total = len(unique_signals)
    returned_signals = unique_signals[: args.max_findings]
    if len(returned_signals) < signal_total:
        warnings.append(
            f"signals truncated to {len(returned_signals)} of {signal_total}; narrow paths or raise --max-findings"
        )

    counts = Counter(signal.kind for signal in unique_signals)
    confidence_counts = Counter(signal.confidence for signal in unique_signals)
    return {
        "schema_version": 1,
        "root": str(cwd),
        "requested_paths": [str(path) for path in roots],
        "extensions": sorted(extensions),
        "files_discovered": len(discovered),
        "files_selected": len(selected),
        "files_scanned": scanned_count,
        "skipped": skipped,
        "signal_total": signal_total,
        "signals_returned": len(returned_signals),
        "counts_by_confidence": dict(sorted(confidence_counts.items())),
        "counts_by_kind": dict(sorted(counts.items())),
        "signals": [asdict(signal) for signal in returned_signals],
        "warnings": sorted(set(warnings)),
        "notice": (
            "Heuristic signals require source-path inspection and behavior proof before refactoring. "
            "Python decision density is AST-derived but is not a repository-configured cyclomatic score; "
            "web-language branch signals are pattern candidates. Do not compare finding counts as complexity metrics."
        ),
    }


def render_text(report: dict[str, object]) -> str:
    signals = report["signals"]
    skipped = report["skipped"]
    warnings = report["warnings"]
    assert isinstance(signals, list)
    assert isinstance(skipped, list)
    assert isinstance(warnings, list)

    lines: list[str] = []
    for signal in signals:
        assert isinstance(signal, dict)
        lines.append(
            f"{str(signal['confidence']).upper():6} {str(signal['kind']):28} "
            f"{signal['path']}:{signal['line']}  {signal['message']}"
        )

    if not lines:
        lines.append("No heuristic signals found. This does not prove the code is simple or safe to refactor.")
    lines.extend(
        (
            "",
            f"Scanned {report['files_scanned']} of {report['files_discovered']} discovered file(s); "
            f"returned {report['signals_returned']} of {report['signal_total']} signal(s).",
        )
    )
    for item in skipped:
        assert isinstance(item, dict)
        lines.append(f"SKIP   {item['path']}: {item['reason']}")
    lines.extend(f"WARN   {warning}" for warning in warnings)
    lines.append(str(report["notice"]))
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", help="Files or folders to scan")
    parser.add_argument(
        "--extensions",
        default=",".join(sorted(DEFAULT_EXTENSIONS)),
        help="Comma-separated file extensions",
    )
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--max-files", type=int, default=500)
    parser.add_argument("--max-findings", type=int, default=500)
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--line-threshold", type=int, default=300)
    parser.add_argument("--function-threshold", type=int, default=30)
    parser.add_argument("--decision-threshold", type=int, default=10)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except (OSError, ValueError) as error:
        print(f"smell_scan: {error}", file=sys.stderr)
        return 2

    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

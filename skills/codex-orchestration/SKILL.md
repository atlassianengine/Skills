---
name: codex-orchestration
description: Start-of-session planning and bounded parallel execution for Codex work in any repository or project. Use when a task can be decomposed into independent investigations, tests, or non-overlapping changes that need one orchestrator to integrate and verify.
---

# Codex orchestration

Use this skill before planning or delegating implementation work in any project. The repository's own `AGENTS.md`, contributor rules, architecture documents, tickets, and toolchain remain authoritative.

## Model roles

- Orchestrator: `GPT 5.6 Sol (Ultra)`
- Executors: `GPT 5.6 Luna (Extra High)`

These are role assignments. Do not claim a model was used unless the runtime actually reports it.

## Start-of-session procedure

1. Read the repository's agent instructions and the project/ticket/architecture guidance they require before code. Do not assume a specific filename or ADR system exists.
2. Identify the underlying problem, risk tier, owning architectural layer, applicable laws/constraints, and smallest useful verification plan.
3. Inspect existing utilities, modules, tickets, and neighboring patterns relevant to the target project.
4. Write an ordered plan with explicit ownership and acceptance criteria.
5. Decide whether delegation reduces time without increasing integration complexity. Keep tiny or tightly coupled work in the orchestrator.

## Delegation procedure

Use 3–5 Luna executors only when the task contains genuinely independent slices, such as separate read-only investigations, isolated tests, or non-overlapping implementation files. Each executor prompt must include:

- exact objective and file boundary;
- relevant project, architecture, and repository-rule context;
- acceptance criteria;
- whether edits are allowed and where;
- required verification commands; and
- required evidence format.

Executors must not silently expand scope, rewrite architecture, or edit overlapping files. They report changed files, commands run, results, failures, and assumptions.

## Integration and completion

The orchestrator remains accountable for the result:

1. Compare each executor result with the plan and repo contracts.
2. Resolve conflicts and make integration edits in the owning layer.
3. Re-check the repository's applicable invariants, plus single-source-of-truth, determinism, boundaries, failure handling, and scope.
4. Run the real repository verification commands, separating implementation evidence from manual/live QA.
5. Report the delegated slices, verification run, and any remaining proof gap. Never report unverified model usage or completion.

## Output contract

Return:

- `goal`: underlying problem;
- `plan`: ordered slices and owners;
- `repo_laws`: repository rules, ADRs, tickets, or equivalent constraints read and applied;
- `delegation`: executor count and bounded scopes, or why delegation was skipped;
- `evidence`: files and verification results; and
- `open_proof`: remaining QA/manual/live evidence, if any.

---
name: codex-orchestration
description: Coordinate bounded parallel Codex work supplied by a user or execution driver while retaining one integration and verification owner. Use when work has independent investigation or implementation slices, delegated residuals must be reconciled, or a staged loop needs forward-cursor discipline; skip tightly coupled, serial, or small work. This skill does not choose project work or worker models.
---

# Codex orchestration

The orchestrator owns the outcome, integration, cross-slice proof, and disposition of every worker residual. Delegation changes who performs a bounded slice; it does not transfer completion accountability.

Repository instructions, the calling driver, architecture law, and routed skills remain authoritative. Preserve the supplied model, reasoning effort, worktree, and no-delegation rule. Never claim a model or tool was used unless the runtime reports it.

## Composition boundary

Orchestration owns how independent work is delegated and integrated. It does not decide which project, ticket, or dependency is next, and it does not choose a worker model from the task type.

- For ad-hoc work, the user's prompt supplies the outcome, boundary, worker profile, and any skills.
- When paired with `$implement-project` or another execution driver, accept only the dependency-ready work IDs, edit boundaries, worker profiles, skills, and proof budgets selected by that driver.
- Do not run project discovery, create execution records, or reinterpret readiness inside this skill. Return evidence and residuals to the driver for canonical reconciliation.

Delegation is opt-in. If neither the user nor a calling driver authorizes sub-agents, keep the work local.

## Orient once

1. State the outcome, done condition, non-goals, risk, and owning architectural seam.
2. Read the repository instructions and only the driver-provided task, ADR, handoff, and source records needed for that outcome.
3. Inspect current owners, callers, consumers, dirty-state boundaries, and the smallest useful verification path before assigning edits.
4. Keep one ordered integration plan with one step in progress.

## Decide whether to delegate

Delegate only when scopes are independent enough to run concurrently without overlapping edits or duplicate conclusions. The worker count follows the number of independent slices and available runtime capacity; do not force a fixed number.

Before spawning, inspect active workers and already accepted findings. Continue or reuse an existing lane when it owns the same boundary; do not create duplicate audit or implementation workers for work already in flight.

Keep work in the orchestrator when it is small, sequential, architecture-coupled, or cheaper to complete than to explain and integrate. If delegation is unavailable, continue directly rather than designing fictional workers.

Useful worker scopes include non-overlapping source areas, focused caller inventories, distinct provider or surface audits, and independent focused tests. Do not delegate the final architecture decision, integration, status reconciliation, or broad test gate.

## Resolve the supplied worker runtime before dispatch

Use Subagent V2 as the standard orchestration runtime. Do not begin with `multi_agent_v1`, infer global model availability from its metadata, or substitute a legacy worker because its tool appears first.

1. Require the user, worker profile, or calling driver to supply the model and reasoning effort. Do not hardcode a default or infer one from whether the lane is implementation, audit, investigation, or review.
2. Use the V2 worker controls for isolation, cancellation, continuation, and handoff. Use a legacy runtime only when the user or an authoritative worker profile explicitly pins it.
3. Record the returned runtime version, model, and effort in dispatch evidence. Verify worker metadata rather than inferring what ran.
4. Never lower effort, switch models, or create user-owned sidebar tasks as a subagent workaround.

Subagent V2 availability is an established harness capability. A V1 tool description is not an availability check and must not redirect orchestration.

If delegation was requested but no worker profile was supplied, do not guess. Keep orientation and boundary work local, then request or return the missing profile before spawning.

## Route skills deliberately

Resolve worker skills before dispatch in this order:

1. skills explicitly named by the user;
2. skills required by repository instructions, the worker profile, or bridge envelope;
3. skills routed by the calling driver, active task, or handoff; and
4. the smallest additional skill genuinely needed for that worker's bounded outcome.

The orchestrator reads each required skill entrypoint before designing the worker envelope. Pass the exact skill name, canonical path, why it applies, and whether it is mandatory; require the worker to confirm it loaded the skill before acting. Do not assume a fork inherited usable skill context. Subagent V2 workers can load locally available skills and their routed references directly; do not paste full skill bodies into prompts unless the worker runtime reports that the files are inaccessible.

Do not send a broad skill bundle, ask workers to browse the whole catalog, invent a task-pinned skill that the project schema does not contain, or use a specialist audit skill merely because its name loosely matches the repository. A worker that discovers a genuinely missing skill should return the need to the orchestrator rather than expanding its own scope.

## Keep the cursor forward

Before dispatching, replaying, or recording work, ask whether the action changes capability, can falsify the changed behavior, or only updates a coordination projection. Coordination state can be substantive when it selects the target or revision, protects authorization or integrity, owns durable recovery, or is the established project execution authority. It must not substitute for implementation or evidence, and stale projection metadata alone must not rewind valid work.

For staged pipelines, migrations, long implementation loops, worker-pool scheduling, or metadata drift, read [references/forward-progress.md](references/forward-progress.md) before replaying accepted work or refilling lanes.

## Worker envelope

Give every worker:

- one outcome and explicit file or system boundary;
- the exact ticket, obligation IDs, architecture clauses, and routed skills that apply;
- allowed edits and forbidden actions;
- the expected positive and negative behavior;
- a narrow verification budget; and
- the evidence and residual format required for handoff.

Workers must not switch models, delegate again, expand scope, edit overlapping files, weaken gates, commit, or mutate project status unless their assigned profile and task explicitly authorize it.

## Verification ownership

Workers verify enough to falsify their own slice: syntax/type correctness, directly affected focused tests, or another narrow gate named in the task. They do not each run workspace-wide builds, full suites, broad audits, or repeated checks merely to look thorough.

Make that budget concrete in each worker envelope. Default to touched-file formatting or syntax plus directly affected positive and negative checks. Do not assign workspace-wide TypeScript checks, full `cargo check`/`cargo test`, repository-wide lint, complete builds, or all-package suites to every worker. A broad gate belongs to a worker only when the task explicitly makes that gate its sole boundary, no narrower check can falsify the slice, or the orchestrator designates exactly one non-editing verification worker.

After integrating all accepted slices, the orchestrator runs the affected integration boundary and any broader gate required by the declared proof class exactly once. Re-run only when integration changed relevant code or a concrete failure requires it. Separate source/focused proof from cold-process, live-provider, migration, contention, browser, deployed, and release proof.

## Integrate and follow through

For each worker result:

1. Inspect the actual diff or evidence against the assigned boundary.
2. Reject scope drift, facade-only work, duplicated authority, weakened tests, and unsupported completion claims.
3. Integrate in dependency order and resolve overlap in the owning layer.
4. Consolidate duplicate observations before doing more research or testing.
5. Triage every residual before finishing or returning it to the calling driver:
   - **current blocker:** required for the present outcome; keep the work open;
   - **separate capability:** different outcome, owner, consumer, surface, provider family, migration seam, or proof subject; create or propose a qualified follow-up in the established project system;
   - **QA or live proof:** route to the QA/release authority without inflating implementation proof;
   - **already owned or unrelated:** link the owner or park it once.

Do not end with an unowned "follow-ups" list. Resolve in-scope blockers and classify every separate item. When a driver owns project traversal, return the qualified residual and evidence to it rather than mutating project records independently.

## Completion

Completion requires the integrated delegated outcome, the declared proof class, and residual classification. A calling driver decides whether that result completes a ticket, work package, project, or audit boundary.

Return a concise handoff containing the outcome, resolved worker profiles and skills, accepted scopes, changed files, verification with proof classes, classified residuals, and remaining external proof. Do not force a rigid schema when prose is clearer.

## Canonical authority and projections

Keep one canonical skill copy and treat other installations as projections. Resolve any link before editing and update the canonical owner. Tool-managed plugin caches are disposable projections and never authorities.

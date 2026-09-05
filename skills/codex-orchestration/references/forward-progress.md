# Forward progress in staged orchestration

Use this reference when work has a persisted cursor, ordered stages, generated intermediates, multiple worker lanes, or coordination metadata that can trigger replay. It does not apply to a short single-owner edit.

## Classify the next action

Classify each proposed action by what it contributes to the declared outcome:

1. **Capability work** changes a producer, consumer, adapter, schema, runtime path, mounted surface, migration seam, or final output.
2. **Falsifying evidence** can reject the changed behavior through a focused test, real consumer path, schema check, conservation check, negative case, benchmark, or another proof required by the task.
3. **Coordination state** routes, schedules, identifies, records, or displays work without itself changing the product behavior.

Prioritize capability and falsifying evidence. Perform coordination work only when it routes the current task, protects a substantive invariant, updates the canonical execution authority, or is itself part of the requested deliverable. Keep duplicate dashboards, copied status, presence markers, and certification-only metadata off the critical path.

Do not infer that all hashes, locks, receipts, or records are administrative. Preserve them when they provide product integrity, input or revision identity, authorization, concurrency safety, durable recovery, release accountability, or the declared proof record.

## Advance the smallest affected cone

Accepted work remains accepted unless current evidence gives a semantic reason to revisit it. Replay or roll back only when at least one condition holds:

- the meaning of an input changed;
- the target, pinned revision, owner, or consumer changed;
- the output is malformed, truncated, nonconserving, inconsistent, or incompatible with its consumer;
- an observed run disproves the earlier result; or
- the changed producer's actual dependency cone reaches that work.

A stale dashboard, duplicate checkbox, missing presence marker, or incompatible administrative projection is not sufficient by itself. Missing substantive evidence blocks the proof claim that requires it; it does not erase unrelated proof already established against unchanged inputs and consumers.

When a coordination gate blocks an otherwise authorized semantic path:

1. inspect the gate's owner and the invariant it protects;
2. preserve and repair it if it controls integrity, authorization, concurrency, recovery, target identity, release safety, or canonical project execution;
3. if it is projection-only, use the narrowest supported semantic path or repair the routing without replaying unaffected work; and
4. remove or downgrade the projection-only dependency only when the current task authorizes that implementation change.

Never use forward progress as permission to bypass security, data-integrity, destructive-action, live-environment, migration, or release gates.

## Schedule by readiness, not waves

- The orchestrator owns the ordered dependency graph, acceptance, integration, publication, cursor movement, and conclusions.
- Keep at most one resource-saturating compiler, full suite, benchmark, migration, server, or long scan running unless the environment explicitly supports more.
- Assign workers only to useful, independent, non-overlapping ready slices. Do not create work to occupy capacity.
- Refill a completed lane when another ready slice exists; do not wait for an arbitrary wave boundary.
- Consume a worker result when its owning dependency is reached and the orchestrator has inspected it. Do not wait for unrelated lanes before advancing.
- If a worker result exposes a blocker on the current dependency path, stop that path, reconcile the blocker, and keep unrelated ready paths moving.

## Report consequence before coordination

Lead the handoff with implemented behavior and falsifying evidence. Report project updates, receipts, dashboards, generated records, and cursor movement separately. A large amount of coordination activity is not throughput unless it changed readiness, protected a substantive invariant, or reconciled an authoritative record required for completion.

---
name: anti-over-engineering
description: Keep significant work on the smallest path that satisfies its real outcome. Use when scope drift, speculative architecture, duplicated testing, or unowned residuals could make a task expand without improving completion; skip tiny tasks and emergency containment.
---

# Anti-over-engineering

Before deep work, record:

```text
OBJECTIVE: one outcome
DONE: observable pass condition
NON-GOALS: adjacent work excluded now
CONSTRAINTS: safety, authority, compatibility, time, and files
```

## Smallest sufficient intervention

Try in order: answer or no change -> existing configuration/workflow -> narrow edit -> new helper or abstraction. Move down only when evidence shows the earlier level cannot satisfy `DONE`.

For each proposed step ask: **If this step fails, can `DONE` still pass?** If yes, park it without investigating it now. Keep no more than five active steps and one step in progress.

Load a tool, skill, reference, or large artifact only when it changes a decision, prevents a known failure, or supplies required proof. Do not invoke everything available "for completeness."

Use one capable agent end to end unless independent scopes make orchestration materially faster. Do not delegate tightly coupled work or create workers merely to repeat searches, reviews, or tests.

## Verification budget

Assign each verification gate one owner.

- An implementation worker runs the narrowest check capable of rejecting its own change.
- The integrator or orchestrator runs cross-slice and broader integration gates once after integration.
- Do not make every worker run the same workspace-wide build, test suite, audit, or residual scan.
- Repeat a check only when code changed after it, its result was ambiguous, or a concrete failure requires a narrower rerun.
- Preserve every security, data-integrity, destructive-action, and release gate required by the governing project.

## Residual triage

Do not let residuals become an endless side quest or an unactionable final list.

1. If the residual prevents `DONE`, keep it in the current scope and do not claim completion.
2. If it is a genuinely separate outcome, owner, consumer, or proof subject, place it in the established project system when authorized; otherwise report the exact proposed destination.
3. If it is unrelated and non-blocking, park it in one line and stop investigating it.
4. If it is already owned elsewhere, link that owner instead of creating another task.

When `DONE` first passes, run one proportional verification pass, reconcile blocking residuals, and stop. "No change needed" is valid when the current system already satisfies the outcome.

Minimalism must never weaken correctness, safety, privacy, authorization, data integrity, required proof, or the user's requested outcome.

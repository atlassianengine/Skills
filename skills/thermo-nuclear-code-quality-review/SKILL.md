---
name: thermo-nuclear-code-quality-review
description: Run an evidence-first, read-only review of a branch, diff, worktree, or implementation for structural maintainability regressions and high-leverage simplifications. Use when the user explicitly asks for a thermo-nuclear, thermonuclear, unusually harsh, or deep structural code-quality review; do not invoke for routine code review.
---

# Thermo-Nuclear Code Quality Review

Find the few structural problems that materially increase system complexity, prove them from the current checkout, and turn each one into an actionable repair with an acceptance test. The goal is not maximal criticism. It is maximal reduction of accidental complexity without changing intended behavior.

## Operating contract

- **Audit is read-only by default.** Inspect and report. Edit only when the user explicitly asks to implement or remediate findings.
- **Resolve the exact target.** Distinguish committed branch changes, staged changes, unstaged changes, and untracked files. Never silently review only `HEAD` when the requested work also exists in the worktree.
- **Preserve checkout boundaries.** Read the applicable repository instructions, identify dirty state, and do not overwrite or attribute unrelated concurrent work.
- **Prove before escalating.** Every finding needs a concrete code path, violated invariant, credible impact, and repair shape. A preference, file length, or unfamiliar pattern alone is not a finding.
- **Inspect the system, not only the patch.** Read full changed files and trace relevant callers, consumers, canonical owners, persistence/effect boundaries, and tests before judging ownership or abstraction quality.
- **Keep proof classes honest.** Source inspection, static checks, focused local tests, cold-process tests, contention tests, live-provider checks, and deployed proof are different evidence classes.
- **Do not create speculative architecture.** Recommend broad restructuring only when it deletes demonstrated complexity, restores an existing boundary, or has at least two concrete consumers.

## Start the review

1. Determine the requested review mode and base:
   - **branch:** merge-base through `HEAD`
   - **worktree:** staged, unstaged, and untracked state
   - **combined:** branch plus worktree, kept separately attributable
   - **focused:** named files, symbols, commit, or subsystem
2. If the helper is available, run it from the target repository. It is read-only and emits JSON metadata, not source contents:

   ```text
   python <skill-dir>/scripts/collect_review_context.py --repo . --base <base-ref> --pretty
   ```

   Omit `--base` only when the user did not name one. The helper reports how it resolved the base; disclose an inferred base in the final review.
3. Read [references/review-method.md](references/review-method.md) completely, then gather the evidence it routes you to. Do not paste or read the entire repository indiscriminately.
4. Maintain a run-local evidence ledger while investigating:

   ```text
   location | observed fact | invariant/impact | proof class | next query
   ```

   Reuse ledger facts instead of repeatedly rediscovering them. Do not publish raw scratch notes unless they help the user verify the conclusion.
5. Falsify each candidate finding: look for an existing owner, helper, validation, transaction, caller constraint, or test that makes the concern invalid. Report only findings that survive.

## Structural review standard

For every meaningful change, ask:

- What invariant is this code trying to preserve, and which layer owns it?
- Does the change add concepts, state, branches, optionality, or indirection that the model could eliminate?
- Is there a **code-judo** move: a smaller ownership or data-model change that deletes whole branches, modes, wrappers, or lifecycle steps?
- Does the implementation reuse the canonical helper and contract, or create a second authority?
- Are UI, state, domain, infrastructure, persistence, and effect responsibilities still flowing in one direction?
- Can partial failure leave committed state, retries, or external effects ambiguous?
- Do types encode valid states, or do booleans, nullable modes, casts, `any`, or `unknown` permit contradictory combinations?
- Did the change make a cohesive file materially harder to scan or push it across 1,000 lines? Treat that threshold as a trigger for a cohesion assessment, not automatic guilt.
- Does the test suite exercise the actual invariant and a negative case, or merely restate the implementation?

Push hardest on:

- parallel sources of truth or duplicated domain rules
- feature checks scattered through shared flows
- partial commits, unfenced retries, non-atomic related writes, or hidden side effects
- missing canonical ownership and cross-layer leakage
- state represented by combinations of flags instead of an explicit model
- generic or pass-through abstractions that hide a simple contract
- serial orchestration that increases failure surface without a dependency reason
- large-file growth caused by mixed responsibilities rather than generated or declarative content
- refactors that move complexity but do not reduce the concepts a maintainer must hold

## Code-judo proposals

A dramatic simplification is useful only when it is concrete. State:

1. the invariant and canonical owner
2. the accidental concepts that disappear
3. the smaller control/data flow
4. compatibility or migration constraints
5. the proof that would establish behavioral parity

Do not prescribe “extract helpers,” “use a state machine,” or “split the file” without naming the resulting ownership boundary and showing what complexity disappears.

## Severity and verdict

Use severity for impact, not rhetorical force:

- **P0:** credible data loss, security boundary failure, or irreversible/system-wide corruption
- **P1:** likely correctness, durability, concurrency, or production-authority failure
- **P2:** concrete structural regression or boundary defect that should be repaired before the change expands
- **P3:** contained maintainability issue with a specific payoff; omit low-value nits

Verdicts:

- **Not approved:** a P0/P1 or merge-blocking structural P2 survives falsification.
- **Approved with follow-ups:** only bounded, non-blocking findings remain.
- **Approved within inspected scope:** no actionable findings remain; proof gaps are still stated.
- **Unable to assess:** essential target evidence is unavailable and cannot be discovered safely.

Passing tests do not erase a structural finding. Conversely, do not block approval on hypothetical elegance or an unproven rewrite.

## Output contract

Lead with the verdict and highest-severity findings. For each finding use:

```text
[P#] Imperative title — path:line
Evidence: exact observed control/data path.
Impact: violated invariant and concrete failure or maintenance cost.
Repair: smallest ownership/model change that removes the cause.
Acceptance: focused proof, including a negative/failure case where relevant.
```

Then include, only when useful:

1. **Scope and proof envelope** — checkout, base/merge-base, branch/worktree portions, commands/tests run, and uninspected areas.
2. **Repair order** — dependency-aware sequence for multiple findings.
3. **Code-judo opportunity** — a high-confidence simplification that is broader than one finding.
4. **Reusable discoveries** — verified canonical owners, invariants, helpers, or proof commands that would save a future reviewer time.
5. **Residual proof gaps** — cold-start, contention, migration, live-provider, recovery, or deployment evidence still missing.

If there are no findings, say so directly. Do not invent comments to make the review look rigorous.

## Agent-accretive behavior

Collect additional evidence only when it reduces uncertainty for the current review or is likely to prevent repeated discovery later. Prefer stable facts such as canonical ownership, durable invariants, known consumer paths, and the narrowest authoritative test command.

Do not silently write review history, memory, tickets, or repository docs. When no authorized durable location exists, include concise **Reusable discoveries** in the result as candidates. Persist them only when the user asks and only in the repository's established authority.

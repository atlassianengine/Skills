---
name: simplify-code-isomorphically
description: Safely simplify existing code by deleting accidental complexity while preserving observable behavior and canonical ownership. Use when the user asks to simplify, refactor, DRY, de-slop, or reduce duplicated state, effects, selectors, layers, types, props, branches, or render churn. Do not use for new feature work or an intentionally behavior-changing redesign.
---

# Simplify Code Isomorphically

A successful simplification leaves fewer concepts, branches, synchronization paths, or ownership ambiguities while preserving the behavior the system and its consumers can observe. Line-count reduction alone is not success.

## Operating contract

- **Follow the user's mode.** A request to simplify or refactor authorizes focused edits. A request to assess, review, or propose remains read-only unless the user also asks for implementation.
- **Resolve the exact target.** Separate requested files/commits from unrelated staged, unstaged, and untracked work. Preserve concurrent changes and checkout boundaries.
- **Read applicable instructions first.** Repository and nested `AGENTS.md` files outrank this generic method. Do not duplicate their project-specific rules into the skill.
- **Preserve the observable contract.** Public APIs, wire/persisted shapes, accepted inputs, outputs, errors, side-effect count/order, durable boundaries, state transitions, ordering, rendered semantics, accessibility, focus, and observable reference identity remain stable unless explicitly authorized otherwise.
- **Trace ownership before moving code.** Inspect callers, consumers, canonical helpers, state owners, persistence/effect owners, and relevant tests. A visually similar block is not proof of shared meaning.
- **High risk raises the proof bar.** Persistence, sync, permissions, auth, migrations, workers, state models, and public contracts are not automatic refusal zones. Keep the change internal and proceed when explicitly in scope and equivalence can be demonstrated; otherwise stop at the boundary and report it.
- **Do not smuggle redesign into cleanup.** If the requested result requires intentional behavior or contract changes, separate that work and label it non-isomorphic.

## Start with an equivalence ledger

Before editing, record only the rows relevant to the target:

```text
surface | current owner | consumers | behavior that must remain | proof
```

Typical surfaces include:

- exported functions, types, props, commands, routes, events, and payloads
- database/schema/wire values and serialization order where contractual
- state transitions, selector output/order, memoization, and reference stability where consumed
- async sequencing, cancellation, retries, idempotency, transactions, and settlement
- DOM structure, accessibility names/states, keyboard/focus behavior, and loading/error states
- date/time, timezone, recurrence, drag, worker, and offline behavior

The ledger is run-local working evidence. Do not publish every row unless it helps verify the result.

## Simplification workflow

1. **Map the target.** Read the diff or named code in full context, then trace the owning layer, direct callers/consumers, and focused tests.
2. **State the simplification thesis.** Name the accidental concepts that will disappear, the canonical owner that remains, the observable contract, risk, and proof. If the proposal adds as many concepts as it removes, revise it.
3. **Establish the safety loop.** Prefer existing characterization tests. If coverage is weak, add the narrowest behavior-level test or keep the change small enough to verify directly. Do not create tautological tests that restate the implementation. When branch pressure materially drives the thesis, read [measured-complexity.md](references/measured-complexity.md) and capture the bounded baseline before editing.
4. **Apply the smallest coherent cut.** Avoid half-migrations that leave old and new authorities active together. Preserve facades and contracts while splitting private responsibilities when that yields a cleaner owner.
5. **Verify equivalence.** Run the narrowest checks that can falsify the thesis, inspect the final diff, search for residue/duplicate authority, and verify negative or failure behavior where relevant.
6. **Stop when saturated.** Finish when the accidental concept is gone, the canonical path is singular, all in-scope consumers are migrated, and remaining uncertainty is a named proof gap rather than another speculative refactor.

## Prefer moves that delete concepts

Use whichever move best fits the real ownership:

1. **Inline** a wrapper that adds no contract, policy, validation, or naming value.
2. **Delete** code proven unused, unreachable, duplicated, or made unnecessary by derivation.
3. **Derive** values from canonical state instead of synchronizing a second copy.
4. **Consolidate** a repeated rule in its existing owner.
5. **Move** behavior to the layer that already owns its invariant or side effects.
6. **Extract** a stable pure transformation or real boundary seam.
7. **Split** private responsibilities behind an unchanged public facade.
8. **Unify** implementations only when domain meaning, lifecycle, failure behavior, permissions, ownership, and future direction match.

Use the deletion test: if an abstraction disappeared, would complexity vanish or simply spill back into callers? Keep only abstractions that reduce what consumers must know.

## Route to one focused lens

Read only the references needed for the active problem:

| Signal | Reference |
| --- | --- |
| AI/codegen residue, fake robustness, shallow wrappers, general smells | [de-slop-and-de-smell.md](references/de-slop-and-de-smell.md) |
| Prop APIs, boolean modes, drilling, slots, primitive forwarding | [de-prop.md](references/de-prop.md) |
| Repeated branches, lookup candidates, duplicated rules, dependency cycles | [de-repeat.md](references/de-repeat.md) |
| Measured branch pressure, complexity hotspots, before/after decision evidence | [measured-complexity.md](references/measured-complexity.md) |
| Mirrored/derived state, competing sources of truth, normalization | [de-state.md](references/de-state.md) |
| Effect-driven derivation, action relays, reset/fetch choreography | [de-effect.md](references/de-effect.md) |
| Redux/Reselect derivation, memoization, parameterized selectors | [de-selector.md](references/de-selector.md) |
| UI/domain/infrastructure ownership leaks | [de-layer.md](references/de-layer.md) |
| Loose contracts, casts, stringly states, runtime/type drift | [de-type.md](references/de-type.md) |
| Rerenders, unstable references, context churn, memoization | [de-render.md](references/de-render.md) |

Read [guidance-examples.md](references/guidance-examples.md) only when a concrete safe/unsafe comparison would resolve ambiguity. Add framework-specific companion skills only when the target actually uses that framework and the refactor depends on its semantics.

Reference “stop conditions” mean stop the current tactic and reassess authorization, ownership, and proof. They do not override an explicit user request to make a broader change; in that case, preserve or deliberately migrate the contract with the required proof.

## Heuristic triage

Use the bundled scanner only to find investigation candidates in the authorized target:

```text
python <skill-dir>/scripts/smell_scan.py <paths...> --format json --max-files 500 --max-findings 200
```

Its confidence labels describe pattern-match confidence, not impact or refactor priority. A scanner signal is never behavior proof and never authorizes an edit. Inspect the full code path and falsify the signal first.

The scanner is not a cross-language cyclomatic-complexity tool. Its Python decision-density signal is AST-derived; its JavaScript, TypeScript, Svelte, and Astro signals are pattern candidates. When an actual complexity score would change the refactor decision, use the repository's configured measurement tool through the measured-complexity lens. Never compare scanner finding counts as though they were complexity scores.

## Risk and proof

Use repository-defined risk tiers when present. Otherwise:

- **Low:** local pure logic, styling, private names, direct wrapper deletion. Verify with diff inspection plus focused static/tests.
- **Medium:** shared components, state, selectors, control flow, async orchestration. Require consumer tracing, characterization, focused tests, and reference/order checks where relevant.
- **High:** persistence, sync, permissions, auth, migrations, workers, durable effects, public/wire contracts. Require contract parity plus failure-path proof; add cold-process, recovery, contention, migration, or live integration evidence only when the affected behavior needs it.

Do not inflate source/static evidence into runtime, cold-process, contention, live-provider, or deployed proof.

## Output contract

Lead with the result. Include:

- **Behavior preserved:** the concrete equivalence contract
- **Simplification:** concepts/branches/state/layers removed and the canonical owner left behind
- **Changed surface:** files, functions, consumers, and public facades affected
- **Risk:** classification and why
- **Verification:** checks run, proof class, and any missing evidence
- **Complexity evidence:** only when branching was material—the bounded subject, tool/configuration, comparable before/after result, and whether the decision footprint actually shrank
- **Skipped:** tempting refactors intentionally left alone because they were unrelated, non-isomorphic, or lacked proof
- **Reusable discoveries:** verified owners, invariants, helpers, or proof commands that would save a future pass time

If no valid simplification exists, say so and give the smallest safe next move. Do not manufacture churn.

## Agent-accretive behavior

Reuse discoveries within the run instead of repeatedly rescanning. Collect additional evidence only when it changes ownership, risk, the simplification thesis, or the proof plan. Prefer durable facts such as canonical owners, accepted contracts, consumer paths, and authoritative test commands. Reuse the discovered complexity command and configuration for the after measurement; do not rescan the repository or switch tools merely to obtain a better number.

Do not silently write memory, tickets, review history, or documentation. Persist reusable discoveries only when the user asks and only in the established project authority.

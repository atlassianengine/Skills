# Measured Complexity Reference

Use this reference only when branching, nesting, repeated decision paths, or a large orchestration function materially drives the simplification thesis. Measurement should reduce agent guesswork; it must not turn a heuristic score into an automatic refactor instruction.

## Agent decision loop

1. **Bound the subject.** Measure the named or touched functions and any helpers that would receive their decisions. Do not scan the entire repository unless the user requested repository-wide triage.
2. **Discover the accepted tool.** Prefer a repository script, linter configuration, CI command, or documented quality gate. Examples include configured ESLint complexity rules, Radon, gocyclo, Lizard, Sonar, or a repository-owned equivalent. Do not install or enable a new gate merely to justify the cleanup.
3. **Capture a comparable baseline.** Record the command, tool/configuration, subject, score, and any parse or coverage exclusions before editing. Use the same tool and configuration afterward.
4. **Classify the decisions.** Separate accidental branching from required domain states, protocol phases, permission boundaries, failure behavior, and explicit orchestration order. A high score does not authorize merging meanings.
5. **Refactor the decision footprint.** Include the original function plus new or changed helpers, predicates, callbacks, lookup tables, and strategies that now carry its choices. Lowering one function's score by scattering the same decisions is not simplification.
6. **Remeasure once the coherent cut is complete.** Compare the same bounded subject. Explain whether maximum local complexity, aggregate decisions, nesting, and consumer knowledge changed; report only dimensions the tool actually provides.
7. **Keep the result only when the system is simpler.** Equivalence proof and canonical ownership outrank the metric. It is valid to retain explicit branches when flattening would hide order, effects, permissions, or failure semantics.

## Threshold policy

- Repository configuration wins.
- Without a configured threshold, rank the authorized functions relative to one another and use the score as investigation priority, not a pass/fail gate.
- Never apply universal rules such as “15 means split.” Language constructs and tools count paths differently, and explicit state machines can be clearer than fragmented helpers.
- Manual counting is acceptable only for a small function when no accepted tool exists. State the counting convention and label the result `estimated`; do not manually score a large mixed-language surface.

## Metric integrity

Reject a claimed improvement when any of these is true:

- branches were compressed into dense boolean expressions or nested ternaries;
- decisions moved into callbacks, predicates, helper functions, strategy objects, macros, generated code, or data without reducing what maintainers and consumers must understand;
- the before and after results use different tools, configurations, parser coverage, or target sets;
- public behavior, branch priority, error propagation, side-effect order, or reference stability changed without authorization;
- only the maximum per-function score improved while the edited decision footprint or ownership ambiguity stayed the same;
- a lookup or strategy table hides materially different permissions, persistence, retry, sync, or failure behavior.

Moving decisions into an existing canonical owner can be a valid improvement even when the local score merely relocates. Name the destination owner and verify that callers now depend on one rule instead of duplicating it.

## Evidence shape

Keep the working record compact:

```text
subject | tool/config | before | after | interpretation
```

Add one note for excluded or unparsed files when that affects confidence. If measurement was unavailable, say `unmeasured` and rely on source-path inspection and behavior proof rather than inventing a score.

Do not publish a complexity table when the metric did not affect the change. When it did, report the bounded decision footprint—not a repository-wide vanity total.

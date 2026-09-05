# Evidence-first review method

Use this method to turn a broad “be harsh” request into a bounded, reproducible review. Adapt the depth to the change's risk and size; do not execute every probe mechanically.

## 1. Establish the review envelope

Record:

- repository root, branch, `HEAD`, and dirty state
- user-specified base or the exact rule used to infer one
- merge-base for branch reviews
- committed branch diff, staged diff, unstaged diff, and untracked files as separate scopes
- nested instructions that apply to changed paths
- generated, vendored, migration, fixture, or lock files that need different interpretation

If the repository is very dirty, do not assume every changed file belongs to the requested work. Use commits, user-named paths, timestamps only as weak hints, and dependency tracing to establish attribution. State unresolved attribution rather than absorbing unrelated work into the verdict.

## 2. Build the change map

Start with names, statuses, line deltas, current line counts, and diff boundaries. Then read:

1. the diff for each in-scope file
2. the complete current file around each changed responsibility
3. definitions and types imported by the changed path
4. direct callers and mounted/runtime consumers
5. the canonical state, domain, persistence, or effect owner
6. tests that claim the invariant

Do not treat plans, comments, status dashboards, generated projections, or Git status as runtime authority. For persisted or wire-facing changes, inspect both production and settlement/readback paths.

## 3. Trace risky paths end to end

Follow the probes that match the change.

### State and branching

- Identify every new state dimension and whether it is canonical or derived.
- Enumerate valid combinations of flags, nullable fields, modes, and status values.
- Trace where each branch is created, consumed, cleared, retried, and recovered.
- Look for repeated predicates that indicate a missing domain model or owner.

### Boundaries and types

- Trace values across UI, state, domain, infrastructure, and persistence boundaries.
- Check whether casts or loose object shapes suppress a contract the type system could state.
- Search for an existing canonical type/helper before accepting a new near-duplicate.
- Verify that abstractions reduce knowledge required by callers; pass-through wrappers do not earn their existence.

### Persistence, effects, and orchestration

- Mark the durable commit boundary and every operation before and after it.
- Ask what happens on timeout, retry, replay, partial success, process death, and concurrent ownership.
- Verify idempotency keys, fencing, transaction scope, and settlement semantics where relevant.
- Treat independent serialized work as a smell only when parallelism also preserves deterministic failure handling.
- Never let a post-commit optional failure make a durable success appear uncommitted.

### File cohesion and decomposition

- A change that moves a file from below 1,000 lines to above it requires an explicit cohesion assessment.
- For an already-large file, measure whether the change adds another responsibility or extends its existing one.
- Exempt generated, declarative, schema, and migration content only when its ownership remains clear.
- Prefer decomposition by responsibility and dependency direction. A file split that preserves the same tangled imports is not a structural improvement.

### Tests and proof

- Locate tests at the owner boundary, not only at the changed helper.
- Require a negative or failure-path case for a newly enforced invariant.
- Detect tautological tests, mocked-away boundaries, regenerated goldens, and demo-path special cases.
- Run the narrowest repository-native checks that can falsify the finding. Do not use fix/write modes during a read-only audit.

## 4. Search for counterfactual compression

For a candidate code-judo move, compare the current and proposed concept sets. A strong proposal deletes concepts such as:

- duplicated state plus synchronization
- a compatibility mode with no real consumer
- repeated branch predicates
- an adapter that only renames fields
- a second retry or lifecycle authority
- UI-owned persistence or domain decisions

Reject a proposal that merely moves the same decisions across more files. Prefer an existing owner over a new manager, framework, registry, or generalized engine.

## 5. Falsify and calibrate

Before reporting a finding:

1. Find the strongest evidence against it.
2. Check whether a caller constraint, transaction, type, or test already preserves the invariant.
3. Verify current line numbers and symbols.
4. Separate observed behavior from inferred risk.
5. Match severity to credible impact and likelihood.
6. Ensure the proposed repair is no larger than the demonstrated problem.

Downgrade or remove findings that depend on imagined future requirements, style preferences, or missing context that is cheap to inspect.

## 6. Track proof classes

Use the narrowest honest label:

- **source:** current code and dependency tracing
- **static:** compiler, linter, schema, or deterministic static analysis
- **focused local:** relevant tests or a warm local runtime
- **cold-process:** restart/readback across a fresh process
- **contention/recovery:** concurrent owners, retries, faults, or crash recovery
- **live integration:** real external provider or integration boundary
- **deployed:** target host/release behavior

Do not convert a lower proof class into a higher one through wording.

## 7. Stop when the review is saturated

The review is saturated when:

- every high-risk changed path has been traced to its canonical owner and relevant consumer
- candidate blockers have been falsified or reported
- file-size and branching hotspots have been assessed in context
- the repair for each finding names an owner and acceptance proof
- remaining uncertainty is captured as a proof gap rather than another speculative finding

Broaden the search only when new evidence changes ownership, impact, or the likely repair. More file reads are not automatically more rigor.

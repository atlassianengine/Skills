# Component analysis and splitting

Use this reference to turn a component tree into actionable ownership decisions. The goal is not the maximum number of components; it is the smallest graph in which each meaningful responsibility has an obvious home.

## Evidence to inspect

For the bounded component or feature, inspect:

- direct route/layout and parent callers;
- imported children and local helpers;
- state, derived values, effects, subscriptions, data loading, persistence, and commands;
- repeated markup and semantically related sibling components;
- shared UI/design-system exports, tokens, variants, and accessibility patterns;
- tests, stories, fixtures, and selectors that define behavior; and
- conditional branches that substantially change structure or ownership.

Do not infer reuse from filenames alone. Search visible labels, roles, CSS/data attributes, imports, and equivalent concepts.

## Structural signals

### God-component pressure

A component deserves decomposition review when several of these coexist:

- it coordinates route or feature state while also implementing detailed child markup;
- unrelated effects, subscriptions, commands, or async lifecycles share one script block;
- several semantic regions can change independently;
- repeated local controls duplicate an established primitive;
- mode booleans produce materially different component structures;
- child-level keyboard, focus, validation, or loading behavior is buried in the parent;
- the component owns both domain decisions and generic visual mechanics; or
- understanding one interaction requires reading most of the file.

None is a line-count threshold. A long cohesive renderer may be correct; a short component with three authorities may not be.

### Over-inlining pressure

Extract or reuse when inline markup represents:

- a domain-neutral primitive already owned by the design system;
- a repeated feature surface with one semantic contract;
- an independently interactive or accessible unit;
- a region with stable inputs but caller-specific content;
- a complex empty/loading/error state reused across callers; or
- a unit whose tests and changes are consistently independent of its parent.

### Over-splitting pressure

Keep or recombine when a proposed child:

- has no meaningful name beyond its HTML tag or position;
- mirrors most of the parent's props or forwards them unchanged;
- requires callback chains for state the parent already owns;
- is used once and has no independent behavior, variation, or change reason;
- separates markup from the styles or semantics that make it understandable; or
- introduces context, a registry, a controller, or a generic schema to avoid a simple local expression.

## Ownership map

| Unit | Owns | Should not own |
| --- | --- | --- |
| Route/page | route data boundary, page-level orchestration, major regions | reusable control internals, duplicated feature policy |
| Feature shell | feature composition and feature-level state coordination | generic UI mechanics already centralized |
| Feature child | one coherent domain surface or interaction | unrelated sibling workflows |
| Shared UI primitive | domain-neutral semantics, accessibility, visual contract, supported variants | feature fetching, persistence, product-specific policy |
| Snippet region | caller-owned markup inside callee-owned framing/iteration | hidden shared state or remote effects |
| Compound context | local state/actions for one related component family | application-global data or infrastructure authority |
| `.svelte.ts` model/controller | coherent nonvisual reactive state, derivation, lifecycle, or commands | visual markup and CSS ownership |
| Inline markup | one-off presentation inseparable from the local composition | repeated semantic components or buried interaction systems |

## Split order

Use this order because each earlier decision can eliminate later machinery:

1. Reuse an existing component without wrapping it when its API fits.
2. Extend the existing owner when one missing variant or snippet seam is the real gap.
3. Separate a coherent nonvisual state/effect owner when UI and lifecycle are entangled.
4. Extract independently meaningful feature children.
5. Add snippet seams for caller-owned regions or item rendering.
6. Introduce compound context only when related descendants truly need shared local state/actions.
7. Migrate all bounded callers and remove the superseded implementation.

## Preflight plan shape

```text
Current graph
- Parent: responsibilities and owners
- Existing shared candidates: fit or mismatch
- Inline regions: keep or extract
- State/effects: current and intended owner

Target graph
- ExistingComponent: reuse/extend and why
- FeatureChild: responsibility and API
- Snippet seam: caller-owned content and callee-owned frame
- Parent: responsibilities that remain
- Removed path: duplicate or obsolete implementation
```

A preflight is incomplete if it proposes filenames without identifying caller migration, state/effect ownership, or the existing shared component search.

## Postflight review

Review the resulting graph from the call site inward:

1. Can the parent be understood as composition without opening every child?
2. Does each child own a coherent behavior or semantic surface?
3. Are props semantic inputs, or are they merely remote controls for internals?
4. Are callbacks named by intent and handled by the true state owner?
5. Are snippets used for caller-owned markup rather than as disguised control flow?
6. Is context limited to one compound family?
7. Did any state, derivation, effect, style, or accessibility behavior become duplicated?
8. Were all in-scope callers migrated and old paths removed?
9. Did the refactor preserve visual and interaction behavior?

Classify each finding as:

- `keep`: current boundary is coherent;
- `reuse`: replace with an established component;
- `extend`: add the smallest missing capability to the existing owner;
- `extract`: create a coherent feature or shared component;
- `recombine`: undo fragmentation that adds indirection;
- `move-state`: establish the correct nonvisual owner;
- `delete`: remove a superseded or duplicated path; or
- `unproven`: requires visual, interaction, accessibility, or runtime evidence.

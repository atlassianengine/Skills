---
name: svelte-composition-patterns
description: Analyze and improve Svelte component boundaries before or after implementation. Use to split god components, replace over-inlined or duplicated UI with existing shared components, design reusable Svelte 5 composition seams, or verify that a refactor produced coherent state, effect, rendering, and child-component ownership without micro-component sprawl.
---

# Svelte composition patterns

## Outcome

Produce a component graph whose ownership is obvious:

- route and feature parents orchestrate rather than absorb every detail;
- state, effects, and derived behavior each have one owner;
- shared UI comes from the established component system;
- feature-specific children own coherent feature surfaces;
- caller-owned visual regions use snippets where that is simpler than prop expansion; and
- extracted APIs make call sites easier to read instead of merely moving lines.

Do not split by line count. Split when ownership, reuse, variation, behavior, or independent change provides a real seam. Keep small one-off markup inline when extraction would only create indirection or prop drilling.

## Choose a mode

- **Preflight:** inspect a component and its surrounding graph, then propose the smallest useful composition plan before implementation.
- **Implement:** perform the requested split or API redesign, reuse existing components, migrate callers, and remove superseded paths.
- **Postflight:** analyze an implementation for remaining god-component responsibilities, over-inlining, duplicate UI, leaky child APIs, or needless fragmentation.
- **API design:** choose among ordinary props, callback props, snippets, compound context, bindable values, DOM delegation, and nonvisual reactive models.

Analysis and Postflight are read-only unless the user also asks for changes.

## Load references conditionally

- Read [analysis-and-splitting.md](references/analysis-and-splitting.md) for Preflight, Postflight, extraction decisions, or component-graph review.
- Read [composition-patterns.md](references/composition-patterns.md) when a selected seam needs a Svelte 5 composition API.
- Read [typing-and-api-boundaries.md](references/typing-and-api-boundaries.md) when implementing or reviewing snippets, wrapper props, callbacks, context, or bindable APIs.

Use official Svelte documentation when syntax or version support is uncertain. Do not load documentation merely to repeat stable project-local conventions.

## Agent workflow

### 1. Discover the real graph

Read the repository instructions and inspect only the relevant neighborhood:

1. the target component;
2. its direct callers or route/layout owner;
3. imported children, controllers/models, actions, stores, and styles;
4. semantically related sibling components; and
5. the established shared UI/design-system directories and exports.

Search by rendered concept, visible label, semantic role, and existing component names before creating anything. A similar component with a different filename still counts as an existing owner.

### 2. Build one component ledger

```text
unit | role | state/effect owner | caller variation | existing reusable owner | seam/problem | disposition
```

Classify each meaningful unit as route composition, feature composition, feature child, shared UI primitive, caller-owned snippet region, nonvisual reactive model/controller, or inline markup.

### 3. Choose the smallest coherent graph

- Reuse or extend an established component when its semantic contract fits.
- Promote a component to shared UI only when it is domain-neutral and follows the existing token, accessibility, export, and variant conventions.
- Keep domain language and feature behavior in a colocated feature component.
- Use a child component for a meaningful visual/behavioral unit with its own contract.
- Use a snippet when the callee owns framing or iteration while the caller owns markup.
- Use context only for one compound component family whose descendants share local state/actions.
- Use a `.svelte.ts` model/controller when nonvisual reactive state or effects form a coherent owner; do not create one merely to make the component file shorter.
- Keep markup inline when it has no independent responsibility, reuse value, variation, or behavioral boundary.

### 4. Implement without creating a second system

Preserve behavior, semantic DOM, keyboard/focus behavior, accessibility relationships, loading/error/empty states, transitions, actions, SSR/hydration behavior, styling hooks, and test selectors unless the task intentionally changes them.

Move each responsibility once, migrate every in-scope caller, and delete obsolete markup/helpers after cutover. Avoid mirror props, pass-through callback chains, duplicated derived state, generic configuration objects, and wrappers that expose nearly every internal option.

Follow the project's Svelte mode and migration scope. For new Svelte 5 runes-mode APIs, prefer `$props`, callback props, snippets with `{@render}`, and deliberate `$bindable` use. Do not convert unrelated legacy components just because they are nearby.

### 5. Verify the resulting graph

Re-read the parent and changed call sites. Confirm that:

- the parent now communicates page/feature composition at a glance;
- every child has a coherent name, responsibility, and API;
- state and effects did not acquire parallel owners;
- shared UI was reused instead of forked;
- no extracted child exists only to hide a few arbitrary lines;
- old paths and duplicate markup are gone; and
- visual, interaction, and accessibility behavior remain intact.

Run the narrow project-native formatter/checker and focused tests for changed behavior. Use `svelte-check` or the repository's equivalent when available. Run broad verification once at the integration owner only when the project requires it.

## Output contract

Return:

- `mode_and_scope`: analyzed components and callers;
- `current_graph`: concise ledger and structural findings;
- `target_graph`: keep, reuse, extend, extract, inline, or delete decisions with reasons;
- `reuse_map`: existing shared components considered and the selected owner;
- `changes`: files and caller migrations, or `read-only`;
- `verification`: commands and observed results; and
- `residuals`: unresolved composition, visual, interaction, or proof gaps.

Do not report success from smaller files alone. Success is a clearer ownership graph, lower duplication, more reusable composition, and preserved behavior.

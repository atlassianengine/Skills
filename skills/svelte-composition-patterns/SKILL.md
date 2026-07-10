---
name: svelte-composition-patterns
description: Svelte 5 component composition patterns for reusable UI APIs, design-system primitives, layout shells, compound components, context providers, snippets, render props, rest-prop delegation, explicit variants, and bindable child APIs. Use when designing or refactoring Svelte components with boolean prop proliferation, slots-to-snippets migration, shared child state, wrapper components, typed snippet props, or headless component APIs.
---

# Svelte Composition Patterns

## Purpose

Use this skill to design Svelte 5 component APIs that stay explicit, typed, and structurally simple. It translates durable composition ideas such as compound components and explicit variants into Svelte-native primitives: snippets, `{@render}`, `$props`, `$state`, `$derived`, `$bindable`, context, and rest props.

Always pair this skill with the official Svelte docs/MCP when writing code. Validate edited `.svelte` files with `svelte-autofixer`.

## Decision Order

1. Identify the owner of state and side effects before designing props.
2. Prefer ordinary props for data and callback props for actions.
3. Use snippets for caller-owned markup and layout regions.
4. Use parameterized snippets when the callee owns data iteration or state and the caller owns rendering.
5. Use context for compound components only when siblings/deep children need one shared state/action contract.
6. Use `$bindable()` only for intentionally two-way component APIs, mostly form controls.
7. Use rest props only to delegate DOM attributes/events to a clear root element.

## Pattern References

Read [references/composition-patterns.md](references/composition-patterns.md) when designing or refactoring component APIs.

Read [references/typing-and-api-boundaries.md](references/typing-and-api-boundaries.md) when typing snippet props, DOM wrapper props, context values, callback props, and bindable props.

## Non-Negotiables

- Do not use `<slot>`, `$$slots`, `<svelte:fragment>`, `export let`, `$$props`, `$$restProps`, or `createEventDispatcher` in new Svelte 5 code.
- Do not add boolean mode props when a named wrapper/variant component can compose the desired structure explicitly.
- Do not mutate unowned props. Use callbacks or `$bindable()` for deliberate shared ownership.
- Do not put style variants in TypeScript utility modules by default. Use component `<style>` blocks, CSS custom properties, and semantic class/data attributes unless the project already has an established class utility.
- Do not create compound-context machinery for a component that only needs `children` or one named snippet.

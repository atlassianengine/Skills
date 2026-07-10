# Typing And API Boundaries

## Props

Define prop types close to the component unless a type is reused across multiple modules. TypeScript is for the component's data/API contract, not for owning CSS styling logic.

```svelte
<script lang="ts">
  interface Props {
    label: string;
    count?: number;
    onReset?: () => void;
  }

  let { label, count = 0, onReset }: Props = $props();
</script>
```

Use `$derived` for values derived from props so updates stay reactive.

```svelte
<script lang="ts">
  let { count = 0 }: { count?: number } = $props();
  const isEmpty = $derived(count === 0);
</script>
```

## Snippets

Import `Snippet` from `svelte`. Snippet parameters are represented as a tuple.

```svelte
<script lang="ts" generics="T">
  import type { Snippet } from 'svelte';

  interface Props {
    items: T[];
    children: Snippet<[T]>;
  }

  let { items, children }: Props = $props();
</script>
```

## DOM Wrapper Props

Use types from `svelte/elements` for wrapper primitives.

```svelte
<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLAnchorAttributes } from 'svelte/elements';

  interface Props extends HTMLAnchorAttributes {
    children: Snippet;
    external?: boolean;
  }

  let { children, external = false, rel, ...rest }: Props = $props();
  const computedRel = $derived(external ? [rel, 'noopener noreferrer'].filter(Boolean).join(' ') : rel);
</script>

<a {...rest} rel={computedRel}>
  {@render children()}
</a>
```

## Callback Props

Use callback props for component-to-parent communication. Name DOM event props as native event names (`onclick`, `oninput`) when forwarding to elements; name domain actions by intent (`onSave`, `onSelect`, `onDismiss`).

```svelte
<script lang="ts">
  interface Props {
    id: string;
    onSelect: (id: string) => void;
  }

  let { id, onSelect }: Props = $props();
</script>

<button type="button" onclick={() => onSelect(id)}>Select</button>
```

## Context

Context is a typed boundary for related components, not a substitute for app architecture.

```ts
import { createContext } from 'svelte';

interface MenuContext {
  open: boolean;
  setOpen(value: boolean): void;
}

export const [getMenuContext, setMenuContext] = createContext<MenuContext>();
```

Use context for local UI families such as tabs, menus, accordions, and command palettes. Keep durable data fetching, persistence, and server communication outside the UI context unless the provider is explicitly an infrastructure adapter.

## Styling Boundary

Prefer this order:

1. Component `<style>` blocks for component-owned styling.
2. CSS custom properties for parent-controlled styling.
3. Semantic class or `data-*` attributes for state and variants.
4. Tailwind utilities in markup when the project uses Tailwind for layout/spacing.
5. TypeScript class builders only when already established and when they reduce duplication without taking ownership of visual design away from CSS.

Avoid TypeScript variant maps for routine component styling in Svelte. They tend to move CSS ownership into `.ts` files and make visual changes harder to inspect.

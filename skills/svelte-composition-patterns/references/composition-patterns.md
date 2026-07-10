# Svelte 5 Composition Patterns

## 1. Snippet Regions

Use snippet props for caller-owned markup. `children` is the implicit default snippet; named snippets replace named slots.

```svelte
<!-- Panel.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';

  interface Props {
    title?: string;
    header?: Snippet;
    children: Snippet;
    footer?: Snippet;
  }

  let { title, header, children, footer }: Props = $props();
</script>

<section class="panel">
  {#if header}
    <header>{@render header()}</header>
  {:else if title}
    <h2>{title}</h2>
  {/if}

  <div class="panel-body">
    {@render children()}
  </div>

  {#if footer}
    <footer>{@render footer()}</footer>
  {/if}
</section>
```

Use this when the parent controls layout content and the child controls framing.

## 2. Parameterized Snippets

Use parameterized snippets when the component owns data flow but the caller owns item rendering.

```svelte
<!-- DataList.svelte -->
<script lang="ts" generics="T">
  import type { Snippet } from 'svelte';

  interface Props {
    items: T[];
    getKey: (item: T) => string | number;
    row: Snippet<[T]>;
    empty?: Snippet;
  }

  let { items, getKey, row, empty }: Props = $props();
</script>

{#if items.length}
  <ul class="data-list">
    {#each items as item (getKey(item))}
      <li>{@render row(item)}</li>
    {/each}
  </ul>
{:else if empty}
  {@render empty()}
{/if}
```

Do not translate React "render props vs children" literally. In Svelte 5, snippets cover both named layout regions and render-prop-style callbacks.

## 3. Explicit Variants

Replace boolean mode props with named components or small wrappers that compose shared pieces.

```svelte
<!-- Bad: one component owns many modes -->
<Composer thread editing showFormatting showAttachments />
```

```svelte
<!-- Better: each variant declares its structure -->
<ThreadComposer channelId={channelId} />
<EditMessageComposer messageId={messageId} />
```

Shared primitives belong underneath:

```svelte
<ComposerFrame>
  <ComposerInput />
  <ComposerToolbar>
    <FormatButton />
    <SubmitButton />
  </ComposerToolbar>
</ComposerFrame>
```

This keeps impossible states out of the prop surface.

## 4. Compound Components With Context

Use context when children/siblings need shared state or actions without prop drilling. Prefer `createContext` for typed access.

```ts
// tabs-context.svelte.ts
import { createContext } from 'svelte';

export interface TabsContext {
  readonly current: string;
  select(id: string): void;
}

export const [getTabs, setTabs] = createContext<TabsContext>();
```

```svelte
<!-- Tabs.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import { setTabs } from './tabs-context.svelte';

  interface Props {
    value: string;
    children: Snippet;
  }

  let { value = $bindable(), children }: Props = $props();

  const tabs = {
    get current() {
      return value;
    },
    select(id: string) {
      value = id;
    },
  };

  setTabs(tabs);
</script>

<div class="tabs">
  {@render children()}
</div>
```

```svelte
<!-- TabTrigger.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import { getTabs } from './tabs-context.svelte';

  interface Props {
    id: string;
    children: Snippet;
  }

  let { id, children }: Props = $props();
  const tabs = getTabs();
  const selected = $derived(tabs.current === id);
</script>

<button
  type="button"
  aria-selected={selected}
  data-selected={selected || undefined}
  onclick={() => tabs.select(id)}
>
  {@render children()}
</button>
```

Keep context values small: state, actions, and metadata needed by the compound family. Do not hide persistence, API calls, or unrelated global state inside a UI context.

## 5. Render Delegation And Rest Props

Use rest props for wrapper primitives that delegate native attributes and event handlers to one underlying element.

```svelte
<!-- Button.svelte -->
<script lang="ts">
  import type { Snippet } from 'svelte';
  import type { HTMLButtonAttributes } from 'svelte/elements';

  interface Props extends HTMLButtonAttributes {
    children: Snippet;
    tone?: 'primary' | 'neutral' | 'danger';
  }

  let {
    children,
    tone = 'primary',
    class: className,
    type = 'button',
    ...rest
  }: Props = $props();
</script>

<button {...rest} {type} class={['button', `button-${tone}`, className]}>
  {@render children()}
</button>
```

Use TypeScript to validate accepted data and DOM attributes. Use CSS to own styling.

## 6. Bindable APIs

Use `$bindable()` when parent and child intentionally share a value.

```svelte
<!-- TextField.svelte -->
<script lang="ts">
  import type { HTMLInputAttributes } from 'svelte/elements';

  interface Props extends Omit<HTMLInputAttributes, 'value'> {
    value: string;
    label: string;
    error?: string;
  }

  let {
    value = $bindable(),
    label,
    error,
    id: providedId,
    ...rest
  }: Props = $props();

  const generatedId = $props.id();
  const id = $derived(providedId ?? generatedId);
</script>

<label for={id}>{label}</label>
<input {...rest} {id} bind:value aria-invalid={error ? 'true' : undefined} />
{#if error}
  <p class="field-error">{error}</p>
{/if}
```

For one-shot actions, use callback props instead of custom events:

```svelte
<script lang="ts">
  interface Props {
    onSubmit: (value: string) => void | Promise<void>;
  }

  let { onSubmit }: Props = $props();
  let value = $state('');
</script>

<button type="button" onclick={() => onSubmit(value)}>Save</button>
```

## 7. Class-Based Reactive Models

Instead of using global writable stores, define standard TypeScript classes with `$state` fields to encapsulate reactive state and business logic. These can be shared globally or injected via context.

```typescript
// countState.svelte.ts
export class CounterModel {
  // Reactive fields
  count = $state(0);
  
  // Reactive derivation
  double = $derived(this.count * 2);

  increment() {
    this.count += 1;
  }

  decrement() {
    this.count -= 1;
  }
}
```

Instantiate and bind directly in Svelte templates:

```svelte
<!-- Counter.svelte -->
<script lang="ts">
  import { CounterModel } from './countState.svelte';
  const model = new CounterModel();
</script>

<button onclick={() => model.decrement()}>-</button>
<span>{model.count} (Double: {model.double})</span>
<button onclick={() => model.increment()}>+</button>
```

## 8. Event Handlers and Modifier Migration

Svelte 5 uses standard HTML event attributes (e.g., `onclick`, `onsubmit`) and has removed template event modifiers (like `on:click|preventDefault`). Call event methods explicitly within your handler functions or use reusable wrapper functions.

```svelte
<!-- Form.svelte -->
<script lang="ts">
  interface Props {
    onsave: () => void;
  }

  let { onsave }: Props = $props();

  function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    event.stopPropagation();
    onsave();
  }
</script>

<form onsubmit={handleSubmit}>
  <button type="submit">Save</button>
</form>
```

Or use a generic utility wrapper:

```typescript
// eventHelpers.ts
export function preventDefault<E extends Event>(fn: (event: E) => void) {
  return function (event: E) {
    event.preventDefault();
    fn(event);
  };
}

// Usage in template:
// <form onsubmit={preventDefault(handleSubmit)}>
```

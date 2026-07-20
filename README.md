# Skills

An installable catalog of skills for Codex and compatible agents.

This repository contains multiple independent skills. Each skill lives under `skills/`.

## Available skills

| Skill | Description | Source |
| --- | --- | --- |
| Simplify Code Isomorphically | Behavior-preserving simplification and refactoring. Removes technical debt, AI slop, and redundancy while preserving external behavior and APIs. | [`skills/simplify-code-isomorphically`](skills/simplify-code-isomorphically) |
| Svelte Composition Patterns | Svelte 5 component composition patterns for reusable UI APIs, design-system primitives, layout shells, snippets, reactive classes, and context. | [`skills/svelte-composition-patterns`](skills/svelte-composition-patterns) |

## Installation

### 1. Simplify Code Isomorphically
```bash
npx skills add atlassianengine/Skills --skill simplify-code-isomorphically
```

### 2. Svelte Composition Patterns
```bash
npx skills add atlassianengine/Skills --skill svelte-composition-patterns
```

### Install All Skills
```bash
npx skills add atlassianengine/Skills
```

## Repository layout

```text
skills/<skill-name>/
  SKILL.md
```

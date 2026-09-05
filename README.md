# Skills

An installable catalog of skills for Codex and compatible agents.

This repository contains multiple independent skills. Each skill lives under `skills/`.

## Available skills

| Skill | Description | Source |
| --- | --- | --- |
| Codex Orchestration | Coordinate bounded parallel Codex work with one integration and verification owner. | [`skills/codex-orchestration`](skills/codex-orchestration) |
| Simplify Code Isomorphically | Safely simplify existing code by deleting accidental complexity while preserving observable behavior and canonical ownership. | [`skills/simplify-code-isomorphically`](skills/simplify-code-isomorphically) |
| Svelte Composition Patterns | Analyze and improve Svelte component boundaries before or after implementation, preserving coherent ownership and avoiding micro-component sprawl. | [`skills/svelte-composition-patterns`](skills/svelte-composition-patterns) |
| Anti Over-Engineering | Keep significant work on the smallest path that proves the real outcome while preventing scope drift and duplicated verification. | [`skills/anti-over-engineering`](skills/anti-over-engineering) |
| Thermo-Nuclear Code Quality Review | Evidence-first structural code-quality review for maintainability regressions and high-leverage simplifications. | [`skills/thermo-nuclear-code-quality-review`](skills/thermo-nuclear-code-quality-review) |

## Installation

### 1. Codex Orchestration
```bash
npx skills add atlassianengine/Skills --skill codex-orchestration
```

### 2. Simplify Code Isomorphically
```bash
npx skills add atlassianengine/Skills --skill simplify-code-isomorphically
```

### 3. Svelte Composition Patterns
```bash
npx skills add atlassianengine/Skills --skill svelte-composition-patterns
```

### 4. Anti Over-Engineering
```bash
npx skills add atlassianengine/Skills --skill anti-over-engineering
```

### 5. Thermo-Nuclear Code Quality Review
```bash
npx skills add atlassianengine/Skills --skill thermo-nuclear-code-quality-review
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

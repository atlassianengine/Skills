# Codex skills

An installable GitHub repository for Codex and compatible agent skills.

Each skill is published as its own scoped npm package through GitHub Packages.
The first package is `@atlassianengine/codex-orchestration`.

## Repository layout

```text
skills/<skill-name>/
  SKILL.md
  README.md
  package.json
```

Create a version tag such as `v0.1.0` to publish the packages through GitHub
Actions.

# Codex orchestration skill

This package contains the `codex-orchestration` skill for Codex-compatible
agents.

## Install from GitHub Packages

Authenticate npm to GitHub Packages with a GitHub personal access token that
has package read access, then install it:

```powershell
npm login --scope=@atlassianengine --registry=https://npm.pkg.github.com
npm install @atlassianengine/codex-orchestration --registry=https://npm.pkg.github.com
```

The installed package contains `SKILL.md` at the package root. Copy that file
into the skill directory used by your agent, or point the agent's skill loader
at the installed package directory.

## Publish

From the repository root:

```powershell
npm publish --workspace @atlassianengine/codex-orchestration
```

Publishing requires `NODE_AUTH_TOKEN` or an npm login for
`https://npm.pkg.github.com`.

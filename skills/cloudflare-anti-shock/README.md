# Cloudflare Anti-Shock

![Runaway Cloudflare usage meets an anti-shock shield; a calm developer works beside a stable usage meter.](assets/anti-shock.png)

One gesture can become hundreds of Durable Object messages, storage writes, retries, and log events. **Cloudflare Anti-Shock** traces that multiplication from a real trigger to every Cloudflare meter it touches, then identifies the smallest change that keeps the feature working.

Use it for a billing spike, a high-frequency feature, or a focused Cloudflare cost and efficiency audit. It covers Workers, Durable Objects and WebSockets, D1, R2, KV, Queues, Workflows, cron, AI, and observability. It separates source-level exposure from measured provider usage and invoiced spend.

```bash
npx skills add atlassianengine/Skills --skill cloudflare-anti-shock
```

Invoke `$cloudflare-anti-shock` with a repository and a named feature or billing metric. The [agent instructions](SKILL.md) link to a product-specific [meter map](references/meter-map.md) and a deterministic [usage scenario helper](scripts/usage-scenario.mjs).

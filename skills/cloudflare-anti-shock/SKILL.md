---
name: cloudflare-anti-shock
description: Audit Cloudflare workloads for runaway cost and unnecessary metered work across Workers, Durable Objects, storage, queues, AI, and observability. Use when asked to investigate a billing spike, audit a high-frequency feature's usage, or reduce Cloudflare spend; not for routine deployment or API guidance.
---

# Cloudflare Anti-Shock

Find the small number of paths where an action, connection, timer, retry, or retained item multiplies Cloudflare usage. Keep required behavior, durability, authorization, and latency intact. An audit is read-only unless the user asks for a repair.

## Route and scope

- **Named feature:** start at its user or system trigger and trace every Cloudflare product it reaches.
- **Billing anomaly:** start with the billed product, metric, resource, environment, and period. Trace backward to triggers. If only a total bill is available, continue a bounded source audit and name the missing usage breakdown rather than assigning the bill to a guess.
- **Broad audit:** inventory deployable entrypoints and configured products, rank paths by trigger frequency, fanout, retries, active lifetime, retained data, and high-unit operations, then inspect one to three paths per wave. Continue waves until meaningful candidates in the requested scope are covered; if the user requested a sample, label the rest uninspected.

Read repository instructions and git status. Establish the target environment, active route or schedule, feature flags, binding/config owner, and plan. If deployment or plan evidence is missing, label source exposure as potential; do not call it active billing. Follow generated or managed configuration when Wrangler files are not the authority. Preserve existing work.

Search within the owning module using bounded file discovery (`rg --files`), then follow configured entrypoints to callers and downstream effects. Include HTTP, service bindings/RPC, WebSocket messages, scheduled handlers, Durable Object alarms, Queue consumers, Workflow steps, backfills, and telemetry. A binding or source file alone does not prove an active path.

Use the [official Cloudflare documentation index](https://developers.cloudflare.com/llms.txt) to reach the relevant product index. Check current official pricing, billing status, lifecycle, and metrics pages for each product actually found; large `llms-full.txt` dumps are not needed. Read only those rows of [meter map](references/meter-map.md) after the products are known. Repository contracts own product behavior and authorization; Cloudflare docs own provider semantics and public rates; account metrics and contracts own actual usage and negotiated pricing.

## Trace and challenge the multiplier

For each candidate, keep a compact ledger:

```text
trigger -> caller -> Cloudflare hop(s) -> storage / AI / observability
environment and enablement | logical actions/month | operations/action | fanout | retries | units/operation | active or retained lifetime
evidence for each factor | required behavior | candidate reduction | disconfirming guard
```

Trace normal, burst, idle, failure/reconnect, replay, and misuse cases. Check duplicate client effects, per-event durable writes, unindexed scans, N+1 reads, repeated cache misses, per-recipient fanout, poison-message retries, overlapping scheduled scans, unnecessary inference, and high-volume logs/spans. Distinguish browser timers from server timers. For WebSockets, separate Worker upgrades, Durable Object incoming messages, protocol pings, active duration, hibernation eligibility, and storage; hibernation does not erase message or downstream charges.

Try to falsify each concern with actual enablement, batching, idempotency, cache policy, indexes, limits, sampling, and tests. Do not turn a grep hit or a generic best practice into a finding. For scheduled work, count the schedule's actual cadence and the items scanned per run, including retries and overlap; a cron expression is a trigger, not its own cost estimate.

## Quantify and decide

Model one logical action first, then keep **each billable meter separate**. Use provider analytics, D1 `meta`, traces, logs, or a reproducible local instrumented path when available. Otherwise label traffic and multiplier assumptions and show a typical and stress case. Model active GB-seconds and stored GB-month separately from request counts. Use `node <skill-dir>/scripts/usage-scenario.mjs <scenario.json>` when multiplication or a before/after comparison merits a deterministic check; read [scenario input](references/scenario.md) first. The helper returns units, not a bill.

Keep topology explicit: count tenants within a deployed service separately from independently scheduled Workers and databases. A shared cron or measurement runs once per deployment; tenant-scoped work scales with the tenants it processes. [GraphQL adaptive datasets can be sampled](https://developers.cloudflare.com/analytics/graphql-api/sampling/); treat grouped and aggregate totals as estimates, inspect sampling metadata when available, and do not force divergent totals to reconcile. Use query `meta` or instrumented runtime to attribute a specific D1 query.

Estimate money only from freshly checked official rates and the actual plan, billing period, account-wide included usage already consumed, rounding, storage class, billing start date, and downstream meters. Published future rates are not current charges. The Workers Paid base subscription is not an incremental saving. If volume, allowance, or negotiated pricing is unknown, report marginal units or an explicit range instead of inventing spend. Distinguish waste within an allowance from likely incremental charges; both may deserve a repair. Alerts and CPU limits can contain exposure but do not remove its cause.

Prioritize the largest credible multiplier and seek the smallest owner-side change that preserves correctness, freshness, history, retry safety, and permissions. If asked to repair, measure a comparable original action-to-meter count, edit the owning layer, and verify a normal action plus a failure/reconnect or retry case. Check that the required behavior still works. Read account metrics only when within the requested scope and repository authority. Do not run live deployments, account mutations, remote product-data reads/writes, or billable probes as a side effect of a local source audit; follow the target repository's release authority when live operations are explicitly in scope.

## Result and stopping rule

Lead with the highest-impact finding that survived falsification, or say none survived **within the inspected scope**. For each finding give `path:line`, the trigger-to-meter trace, observed or assumed units/action and period, stress case, plan/rate source and check date if quoting money, existing guards, a capability-preserving repair, and a comparable acceptance counter. Name the strongest proof class: source exposure, local runtime, provider usage, or invoice. Do not present source arithmetic as a measured bill or a proposed change as realized savings.

Use P0 for credible unbounded active cost or system-wide failure, P1 for likely material runaway usage, P2 for concrete repeated overuse, and P3 only for a contained issue with a meaningful payoff. Finish with covered and uninspected paths/products and the exact metric that would resolve any account-level gap. If a path is disabled, label it dormant in that environment and move to the next active candidate. If a price cannot be verified, leave dollars out and continue the usage trace.

Completion means the named path's downstream meters and failure modes are accounted for, the billing anomaly is reconciled or its missing counter identified, or the requested broad scope's meaningful candidates are inspected with exclusions explicit. A clean path is never evidence that the entire account is cost-safe.

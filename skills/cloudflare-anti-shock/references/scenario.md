# Usage scenario helper

Use this only after tracing the real path. Run `node <skill-dir>/scripts/usage-scenario.mjs <scenario.json>` for one current scenario. Add a second scenario only when a specific capability-preserving repair is supported by the trace. The helper performs arithmetic; it does not know Cloudflare billing rules, included usage, or prices.

The JSON `scenarios` array accepts one or two entries. Each scenario contains a unique `name` and one or more `workloads`. A workload has a stable logical `name`, `eventsPerMonth`, a `basis` describing measured or assumed traffic, and at least one `meter`. A meter has `product`, `metric`, a `basis` for its factors, `callsPerEvent`, `fanout`, `attempts`, and `unitsPerCall`. All numeric factors must be finite and nonnegative; `fanout`, `attempts`, and `unitsPerCall` must be positive. Use the actual billable unit, not an unlabeled generic “call.” Add a separate meter for every downstream metric. Put product-specific conversion into the meter basis and factors: for example, D1 scanned rows per query, Queue payload chunks, Durable Object active GB-seconds, or sampled log events. Do not enter raw WebSocket messages as billed DO requests without checking the current conversion rule.

For two scenarios, workload names, event counts, traffic basis, and product/metric keys must match. If the repair removes an operation, retain its meter with `callsPerEvent: 0` and explain why. If the repair adds another cost, include that meter in both scenarios with zero calls on the current path. This makes omitted costs detectable. The script reports monthly units and reductions, with no pricing or provider proof.

```json
{
  "scenarios": [
    {
      "name": "current",
      "workloads": [{
        "name": "editing session",
        "basis": "assumed 10000 editing sessions/month",
        "eventsPerMonth": 10000,
        "meters": [{
          "product": "Workers", "metric": "requests",
          "basis": "hypothetical HTTP autosave on each of 100 edits/session",
          "callsPerEvent": 100, "fanout": 1, "attempts": 1, "unitsPerCall": 1
        }]
      }]
    },
    {
      "name": "candidate",
      "workloads": [{
        "name": "editing session",
        "basis": "assumed 10000 editing sessions/month",
        "eventsPerMonth": 10000,
        "meters": [{
          "product": "Workers", "metric": "requests",
          "basis": "hypothetical coalesced save after the same 100 edits",
          "callsPerEvent": 1, "fanout": 1, "attempts": 1, "unitsPerCall": 1
        }]
      }]
    }
  ]
}
```

This arithmetic yields 1,000,000 versus 10,000 Worker requests for the stated assumptions. It proves nothing about an actual implementation, bill, or whether one save per session preserves required durability. Do not use an assumed candidate as a claimed saving.

For an idle-duration or retained-storage meter, define the workload as one month (`eventsPerMonth: 1`) and explain the object count and GB-second or GB-month derivation in `basis`. Do not multiply a monthly stock meter by the number of user actions. Keep the meter names and workload traffic identical across comparison scenarios; if the proposed path changes traffic, show it as a separate assumption rather than hiding it in the comparison.

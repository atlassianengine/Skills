#!/usr/bin/env node
import { readFileSync } from 'node:fs';

function fail(message) {
  throw new Error(message);
}

function nonnegative(value, where) {
  if (typeof value !== 'number' || !Number.isFinite(value) || value < 0) {
    fail(`${where} must be a finite nonnegative number`);
  }
  return value;
}

function positive(value, where) {
  const number = nonnegative(value, where);
  if (number === 0) fail(`${where} must be greater than zero`);
  return number;
}

function label(value, where) {
  if (typeof value !== 'string' || value.trim() === '') fail(`${where} must be a nonempty string`);
  return value.trim();
}

function safeProduct(values, where) {
  const result = values.reduce((product, value) => product * value, 1);
  if (!Number.isFinite(result) || result > Number.MAX_SAFE_INTEGER) {
    fail(`${where} exceeds safe numeric range; split the workload`);
  }
  return result;
}

function readScenario(raw, index) {
  const where = `scenarios[${index}]`;
  const name = label(raw?.name, `${where}.name`);
  if (!Array.isArray(raw?.workloads) || raw.workloads.length === 0) {
    fail(`${where}.workloads must be a nonempty array`);
  }
  const workloads = raw.workloads.map((workload, workloadIndex) => {
    const path = `${where}.workloads[${workloadIndex}]`;
    const workloadName = label(workload?.name, `${path}.name`);
    const basis = label(workload?.basis, `${path}.basis`);
    const eventsPerMonth = nonnegative(workload?.eventsPerMonth, `${path}.eventsPerMonth`);
    if (!Array.isArray(workload?.meters) || workload.meters.length === 0) {
      fail(`${path}.meters must be a nonempty array`);
    }
    const meters = workload.meters.map((meter, meterIndex) => {
      const meterPath = `${path}.meters[${meterIndex}]`;
      const product = label(meter?.product, `${meterPath}.product`);
      const metric = label(meter?.metric, `${meterPath}.metric`);
      const basis = label(meter?.basis, `${meterPath}.basis`);
      const callsPerEvent = nonnegative(meter?.callsPerEvent, `${meterPath}.callsPerEvent`);
      const fanout = positive(meter?.fanout, `${meterPath}.fanout`);
      const attempts = positive(meter?.attempts, `${meterPath}.attempts`);
      const unitsPerCall = positive(meter?.unitsPerCall, `${meterPath}.unitsPerCall`);
      const monthlyUnits = safeProduct(
        [eventsPerMonth, callsPerEvent, fanout, attempts, unitsPerCall],
        meterPath,
      );
      return { product, metric, basis, callsPerEvent, fanout, attempts, unitsPerCall, monthlyUnits };
    });
    const meterKeys = meters.map(({ product, metric }) => JSON.stringify([product, metric]));
    if (new Set(meterKeys).size !== meterKeys.length) fail(`${path}.meters contains duplicate product/metric pairs`);
    return { name: workloadName, basis, eventsPerMonth, meters };
  });
  const names = workloads.map((workload) => workload.name);
  if (new Set(names).size !== names.length) fail(`${where}.workloads contains duplicate names`);
  const totals = new Map();
  for (const workload of workloads) {
    for (const meter of workload.meters) {
      const key = JSON.stringify([meter.product, meter.metric]);
      const next = (totals.get(key) ?? 0) + meter.monthlyUnits;
      if (!Number.isFinite(next) || next > Number.MAX_SAFE_INTEGER) fail(`total ${key} exceeds safe numeric range`);
      totals.set(key, next);
    }
  }
  return { name, workloads, totals };
}

function main() {
  if (process.argv.length === 3 && ['--help', '-h'].includes(process.argv[2])) {
    process.stdout.write('usage: node usage-scenario.mjs <scenario.json>\nModel one current path or two comparable paths; output monthly units, not a bill.\n');
    return;
  }
  if (process.argv.length !== 3) fail('usage: node usage-scenario.mjs <scenario.json>');
  const input = JSON.parse(readFileSync(process.argv[2], 'utf8'));
  if (!Array.isArray(input?.scenarios) || input.scenarios.length < 1 || input.scenarios.length > 2) {
    fail('scenarios must contain one current path or two comparable paths');
  }
  const scenarios = input.scenarios.map(readScenario);
  const [before, after] = scenarios;
  if (after) {
    if (before.name === after.name) fail('scenario names must differ');
    const beforeWorkloads = new Map(before.workloads.map((workload) => [workload.name, workload]));
    if (beforeWorkloads.size !== after.workloads.length) fail('both paths must have the same workloads');
    for (const workload of after.workloads) {
      const original = beforeWorkloads.get(workload.name);
      if (!original || original.eventsPerMonth !== workload.eventsPerMonth || original.basis !== workload.basis) {
        fail(`workload ${workload.name} must have the same monthly events and basis in both paths`);
      }
      const keys = (meters) => meters.map(({ product, metric }) => JSON.stringify([product, metric])).sort();
      if (JSON.stringify(keys(original.meters)) !== JSON.stringify(keys(workload.meters))) {
        fail(`workload ${workload.name} must name the same product/metric pairs in both paths; use zero calls for removed work`);
      }
    }
  }
  const totals = (scenario) => [...scenario.totals.entries()].sort(([a], [b]) => a.localeCompare(b)).map(([key, monthlyUnits]) => {
    const [product, metric] = JSON.parse(key);
    return { product, metric, monthlyUnits };
  });
  const comparison = after ? [...before.totals.keys()].sort().map((key) => {
    const [product, metric] = JSON.parse(key);
    const beforeUnits = before.totals.get(key) ?? 0;
    const afterUnits = after.totals.get(key) ?? 0;
    return {
      product,
      metric,
      beforeUnits,
      afterUnits,
      changeUnits: afterUnits - beforeUnits,
      reductionPercent: beforeUnits === 0 ? null : ((beforeUnits - afterUnits) / beforeUnits) * 100,
    };
  }) : undefined;
  process.stdout.write(`${JSON.stringify({
    proofClass: 'scenario arithmetic only; no pricing or observed bill',
    scenarios: scenarios.map((scenario) => ({ name: scenario.name, workloads: scenario.workloads, totals: totals(scenario) })),
    ...(comparison ? { comparison } : {}),
  }, null, 2)}\n`);
}

try {
  main();
} catch (error) {
  process.stderr.write(`${error instanceof Error ? error.message : String(error)}\n`);
  process.exitCode = 1;
}

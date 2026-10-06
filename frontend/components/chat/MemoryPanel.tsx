"use client";

import { useCallback, useEffect, useState } from "react";
import { Brain, RefreshCw } from "lucide-react";

import { fetchMemory, fetchTrace } from "@/lib/api";
import type { MemoryFact, ToolRun } from "@/lib/chatTypes";

export function MemoryPanel({ refreshKey }: { refreshKey?: number }) {
  const [facts, setFacts] = useState<MemoryFact[]>([]);
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [runs, setRuns] = useState<ToolRun[]>([]);

  const load = useCallback(async () => {
    const m = await fetchMemory();
    setFacts(m.facts ?? []);
    setCounts(m.counts ?? {});
    const t = await fetchTrace();
    setRuns(t.tool_runs ?? []);
  }, []);

  useEffect(() => {
    void load();
  }, [load, refreshKey]);

  return (
    <div className="card p-4">
      <div className="mb-2 flex items-center justify-between">
        <h2 className="flex items-center gap-2 text-sm font-semibold">
          <Brain className="h-4 w-4" /> Memory
        </h2>
        <button className="btn btn-ghost !px-2 !py-1" onClick={() => void load()} aria-label="Refresh">
          <RefreshCw className="h-3.5 w-3.5" />
        </button>
      </div>
      <div className="mb-3 flex flex-wrap gap-1.5">
        {Object.entries(counts).map(([k, v]) => (
          <span key={k} className="chip">{k}: {v}</span>
        ))}
      </div>
      <h3 className="mb-1 text-xs font-semibold uppercase tracking-wide" style={{ color: "var(--muted)" }}>
        Facts
      </h3>
      <ul className="mb-3 space-y-1 text-sm">
        {facts.length ? facts.slice(0, 25).map((f) => (
          <li key={f.id} className="flex gap-2">
            <span title={f.source} style={{ color: f.source === "explicit" ? "#38b36b" : "var(--muted)" }}>.</span>
            <span>{f.text}</span>
          </li>
        )) : <li style={{ color: "var(--muted)" }}>No memories yet.</li>}
      </ul>
      <h3 className="mb-1 text-xs font-semibold uppercase tracking-wide" style={{ color: "var(--muted)" }}>
        Recent tools
      </h3>
      <ul className="space-y-1 text-xs font-mono" style={{ color: "var(--muted)" }}>
        {runs.slice(0, 12).map((r, i) => (
          <li key={i}>{r.ok ? "+" : "x"} {r.tool}</li>
        ))}
      </ul>
    </div>
  );
}

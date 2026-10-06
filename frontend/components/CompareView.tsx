"use client";

import { useState } from "react";
import { GitCompare, Plus, RotateCcw, Square, X } from "lucide-react";

import { useApiKeys } from "@/contexts/ApiKeyContext";
import { useResearch } from "@/contexts/ResearchContext";
import { PROVIDERS, providerById } from "@/lib/models";
import type { Provider, ResearchState } from "@/lib/types";
import { ProgressStages } from "./ProgressStages";
import { ReportView } from "./ReportView";

interface Sel {
  provider: Provider;
  model: string;
}

function timing(c: ResearchState): string {
  if (!c.startedAt) return "";
  const ms = (c.finishedAt ?? Date.now()) - c.startedAt;
  return `${(ms / 1000).toFixed(1)}s`;
}

export function CompareView() {
  const { keys, hasKey } = useApiKeys();
  const { compareQuery, compareColumns, runCompare, stopCompare, resetCompare } = useResearch();

  const [query, setQuery] = useState(compareQuery);
  const [sels, setSels] = useState<Sel[]>([
    { provider: "openai", model: providerById("openai").defaultModel },
    { provider: "anthropic", model: providerById("anthropic").defaultModel },
  ]);
  const [maxSub, setMaxSub] = useState(4);
  const [search, setSearch] = useState(true);
  const [warn, setWarn] = useState<string | null>(null);

  const running = compareColumns.some((c) => c.running);

  const addSel = () =>
    setSels((s) =>
      s.length >= 4 ? s : [...s, { provider: "kimi", model: providerById("kimi").defaultModel }],
    );
  const removeSel = (i: number) => setSels((s) => s.filter((_, idx) => idx !== i));
  const setSel = (i: number, provider: Provider, model: string) =>
    setSels((s) => s.map((x, idx) => (idx === i ? { provider, model } : x)));

  const submit = () => {
    const q = query.trim();
    if (q.length < 3) {
      setWarn("Enter a question (at least 3 characters).");
      return;
    }
    const missing = [...new Set(sels.filter((s) => !hasKey(s.provider)).map((s) => providerById(s.provider).label))];
    if (missing.length) {
      setWarn(`Missing API keys for: ${missing.join(", ")}. Add them with the Keys button.`);
      return;
    }
    setWarn(null);
    runCompare(
      q,
      sels.map((s) => ({ provider: s.provider, model: s.model, apiKey: keys[s.provider]! })),
      { maxSubquestions: maxSub, search },
    );
  };

  return (
    <div className="space-y-5">
      <section className="pt-6">
        <h1 className="text-2xl font-semibold">Compare models</h1>
        <p className="mt-1 text-sm" style={{ color: "var(--muted)" }}>
          Run the same question across up to four models and see the reports and timing side by side.
        </p>
      </section>

      <div className="card p-4">
        <textarea
          className="input min-h-[80px] resize-y"
          placeholder="Ask one question to run on every selected model..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="mt-3 space-y-2">
          {sels.map((s, i) => (
            <div key={i} className="flex flex-wrap items-center gap-2">
              <select
                className="input !w-auto"
                value={s.provider}
                onChange={(e) => {
                  const p = e.target.value as Provider;
                  setSel(i, p, providerById(p).defaultModel);
                }}
              >
                {PROVIDERS.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.label}
                  </option>
                ))}
              </select>
              <select
                className="input !w-auto"
                value={s.model}
                onChange={(e) => setSel(i, s.provider, e.target.value)}
              >
                {providerById(s.provider).models.map((m) => (
                  <option key={m} value={m}>
                    {m}
                  </option>
                ))}
              </select>
              <span className="chip">
                <span
                  className="h-2 w-2 rounded-full"
                  style={{ background: hasKey(s.provider) ? "#38b36b" : "#d4a017" }}
                />
                {hasKey(s.provider) ? "key set" : "no key"}
              </span>
              {sels.length > 1 && (
                <button className="btn btn-ghost !px-2" onClick={() => removeSel(i)} aria-label="Remove">
                  <X className="h-4 w-4" />
                </button>
              )}
            </div>
          ))}
          {sels.length < 4 && (
            <button className="btn btn-ghost" onClick={addSel}>
              <Plus className="h-4 w-4" /> Add model
            </button>
          )}
        </div>

        <div className="mt-3 flex flex-wrap items-center gap-4">
          <label className="flex items-center gap-2 text-sm" style={{ color: "var(--muted)" }}>
            <span>Depth</span>
            <input
              type="range"
              min={1}
              max={8}
              value={maxSub}
              onChange={(e) => setMaxSub(Number(e.target.value))}
            />
            <span className="tabular-nums">{maxSub}</span>
          </label>
          <label className="flex items-center gap-2 text-sm" style={{ color: "var(--muted)" }}>
            <input type="checkbox" checked={search} onChange={(e) => setSearch(e.target.checked)} />
            Live web search
          </label>
          <div className="ml-auto flex items-center gap-2">
            {running ? (
              <button className="btn btn-ghost" onClick={stopCompare}>
                <Square className="h-4 w-4" /> Stop
              </button>
            ) : (
              <button className="btn btn-primary" onClick={submit}>
                <GitCompare className="h-4 w-4" /> Run compare
              </button>
            )}
            {compareColumns.length > 0 && !running && (
              <button className="btn btn-ghost" onClick={resetCompare}>
                <RotateCcw className="h-4 w-4" /> Clear
              </button>
            )}
          </div>
        </div>
        {warn && (
          <p className="mt-2 text-sm" style={{ color: "#d9534f" }}>
            {warn}
          </p>
        )}
      </div>

      {compareColumns.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          {compareColumns.map((c, i) => (
            <div key={i} className="space-y-3">
              <div className="flex items-center justify-between gap-2">
                <div className="font-medium">
                  {c.provider} · {c.model}
                </div>
                <span className="chip tabular-nums">{timing(c)}</span>
              </div>
              <ProgressStages state={c} />
              {c.error && (
                <div className="card p-3" style={{ borderColor: "#d9534f" }}>
                  <p className="text-sm" style={{ color: "#d9534f" }}>
                    {c.error}
                  </p>
                </div>
              )}
              <ReportView state={c} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

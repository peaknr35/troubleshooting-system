"use client";

import type { ResearchState } from "@/lib/types";
import { ExportMenu } from "./ExportMenu";
import { Markdown } from "./Markdown";
import { SourceList } from "./SourceList";

export function ReportView({ state }: { state: ResearchState }) {
  const visible = state.report || state.stage === "report" || state.stage === "done";
  if (!visible) return null;
  return (
    <div className="card p-5">
      <div className="mb-3 flex flex-wrap items-center justify-between gap-3">
        <h2 className="text-lg font-semibold">Report</h2>
        {state.stage === "done" && state.report && <ExportMenu state={state} />}
      </div>
      {state.report ? (
        <Markdown>{state.report}</Markdown>
      ) : (
        <p className="text-sm" style={{ color: "var(--muted)" }}>
          Writing the report...
        </p>
      )}
      {state.reportSources?.length > 0 && (
        <div className="mt-5 border-t pt-4" style={{ borderColor: "var(--border)" }}>
          <h3 className="mb-2 text-sm font-semibold">Sources</h3>
          <SourceList sources={state.reportSources} />
        </div>
      )}
    </div>
  );
}

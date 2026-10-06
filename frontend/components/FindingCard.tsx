"use client";

import { useState } from "react";
import { ChevronDown, ChevronRight } from "lucide-react";

import type { Finding } from "@/lib/types";
import { Markdown } from "./Markdown";
import { SourceList } from "./SourceList";

export function FindingCard({ finding, defaultOpen }: { finding: Finding; defaultOpen?: boolean }) {
  const [open, setOpen] = useState(defaultOpen ?? false);
  return (
    <div className="card p-4">
      <button className="flex w-full items-center gap-2 text-left" onClick={() => setOpen((o) => !o)}>
        {open ? (
          <ChevronDown className="h-4 w-4 shrink-0" />
        ) : (
          <ChevronRight className="h-4 w-4 shrink-0" />
        )}
        <span className="font-medium">{finding.subquestion}</span>
      </button>
      {open && (
        <div className="mt-3 space-y-3">
          {finding.summary ? (
            <Markdown>{finding.summary}</Markdown>
          ) : (
            <p className="text-sm" style={{ color: "var(--muted)" }}>
              Researching...
            </p>
          )}
          {finding.sources?.length > 0 && (
            <div>
              <p
                className="mb-1 text-xs font-semibold uppercase tracking-wide"
                style={{ color: "var(--muted)" }}
              >
                Sources
              </p>
              <SourceList sources={finding.sources} />
            </div>
          )}
        </div>
      )}
    </div>
  );
}

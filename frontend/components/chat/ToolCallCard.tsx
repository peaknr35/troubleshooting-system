"use client";

import { useState } from "react";
import { Check, ChevronDown, ChevronRight, Loader2, X } from "lucide-react";

import type { ToolActivity } from "@/lib/chatTypes";

export function ToolCallCard({ tool }: { tool: ToolActivity }) {
  const [open, setOpen] = useState(false);
  return (
    <div className="rounded-lg border px-3 py-2 text-sm"
         style={{ borderColor: "var(--border)", background: "var(--surface-2)" }}>
      <button className="flex w-full items-center gap-2 text-left" onClick={() => setOpen((o) => !o)}>
        {open ? <ChevronDown className="h-3.5 w-3.5" /> : <ChevronRight className="h-3.5 w-3.5" />}
        <span className="font-mono font-medium">{tool.name}</span>
        {tool.running ? (
          <Loader2 className="h-3.5 w-3.5 animate-spin" style={{ color: "var(--accent)" }} />
        ) : tool.ok === false ? (
          <X className="h-3.5 w-3.5" style={{ color: "#d9534f" }} />
        ) : (
          <Check className="h-3.5 w-3.5" style={{ color: "#38b36b" }} />
        )}
      </button>
      {open && (
        <div className="mt-2 space-y-2">
          {tool.args != null && (
            <pre className="overflow-x-auto rounded p-2 text-xs" style={{ background: "rgba(0,0,0,0.2)" }}>
              {JSON.stringify(tool.args, null, 2)}
            </pre>
          )}
          {tool.result && (
            <pre className="max-h-48 overflow-auto whitespace-pre-wrap rounded p-2 text-xs"
                 style={{ background: "rgba(0,0,0,0.2)" }}>
              {tool.result}
            </pre>
          )}
        </div>
      )}
    </div>
  );
}

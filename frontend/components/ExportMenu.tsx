"use client";

import { useState } from "react";
import { Check, Copy, FileText, Loader2 } from "lucide-react";

import { copyForDocs, createGoogleDoc, isGoogleConfigured } from "@/lib/googleDocs";
import type { ResearchState } from "@/lib/types";

export function ExportMenu({ state }: { state: ResearchState }) {
  const [copied, setCopied] = useState(false);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);

  const onCopy = async () => {
    setErr(null);
    try {
      await copyForDocs(state);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setErr("Copy failed.");
    }
  };

  const onCreate = async () => {
    setErr(null);
    setBusy(true);
    try {
      const url = await createGoogleDoc(state);
      window.open(url, "_blank", "noreferrer");
    } catch (e: any) {
      setErr(e?.message ?? "Could not create the document.");
    } finally {
      setBusy(false);
    }
  };

  const configured = isGoogleConfigured();
  return (
    <div className="flex flex-wrap items-center gap-2">
      <button className="btn btn-ghost" onClick={onCopy}>
        {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
        {copied ? "Copied" : "Copy for Google Docs"}
      </button>
      <button
        className="btn btn-ghost"
        onClick={onCreate}
        disabled={busy || !configured}
        title={configured ? "Create a Google Doc" : "Set NEXT_PUBLIC_GOOGLE_CLIENT_ID to enable"}
      >
        {busy ? <Loader2 className="h-4 w-4 animate-spin" /> : <FileText className="h-4 w-4" />}
        Create Google Doc
      </button>
      {err && (
        <span className="text-xs" style={{ color: "#d9534f" }}>
          {err}
        </span>
      )}
    </div>
  );
}

"use client";

import { useRef, useState } from "react";
import { Download, ExternalLink, Eye, EyeOff, Trash2, Upload, X } from "lucide-react";

import { useApiKeys } from "@/contexts/ApiKeyContext";
import { PROVIDERS } from "@/lib/models";
import type { Provider } from "@/lib/types";

export function ApiKeyManager({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { keys, setKey, clearAll, importFromJson, exportJson } = useApiKeys();
  const [show, setShow] = useState<Record<string, boolean>>({});
  const [msg, setMsg] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  if (!open) return null;

  const onExport = () => {
    const blob = new Blob([exportJson()], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "deep-research-keys.json";
    a.click();
    URL.revokeObjectURL(url);
    setMsg("Exported keys to a JSON file.");
  };

  const onImportFile = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    try {
      importFromJson(await file.text());
      setMsg("Keys imported.");
    } catch {
      setMsg("Could not parse that file. Expected JSON like { \"openai\": \"sk-...\" }.");
    }
    e.target.value = "";
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center overflow-y-auto bg-black/40 p-4 sm:p-8"
      onClick={onClose}
    >
      <div className="card w-full max-w-lg p-5" onClick={(e) => e.stopPropagation()}>
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-lg font-semibold">API keys</h2>
          <button className="btn btn-ghost !px-2" onClick={onClose} aria-label="Close">
            <X className="h-4 w-4" />
          </button>
        </div>

        <p className="mb-4 text-sm" style={{ color: "var(--muted)" }}>
          Keys are stored only in this browser (localStorage) and are sent with each
          request to the provider you choose. They are never stored on our servers.
        </p>

        <div className="space-y-4">
          {PROVIDERS.map((p) => {
            const id = p.id as Provider;
            const visible = show[id];
            return (
              <div key={id}>
                <div className="mb-1 flex items-center justify-between">
                  <label className="text-sm font-medium">{p.label}</label>
                  <a
                    href={p.getKeyUrl}
                    target="_blank"
                    rel="noreferrer"
                    className="inline-flex items-center gap-1 text-xs"
                    style={{ color: "var(--accent)" }}
                  >
                    Get a key <ExternalLink className="h-3 w-3" />
                  </a>
                </div>
                <div className="flex items-center gap-2">
                  <input
                    className="input font-mono"
                    type={visible ? "text" : "password"}
                    placeholder={p.keyHint}
                    value={keys[id] ?? ""}
                    onChange={(e) => setKey(id, e.target.value)}
                    autoComplete="off"
                    spellCheck={false}
                  />
                  <button
                    className="btn btn-ghost !px-2"
                    onClick={() => setShow((s) => ({ ...s, [id]: !s[id] }))}
                    aria-label={visible ? "Hide" : "Show"}
                  >
                    {visible ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>
            );
          })}
        </div>

        <div className="mt-5 flex flex-wrap items-center gap-2">
          <button className="btn btn-ghost" onClick={() => fileRef.current?.click()}>
            <Upload className="h-4 w-4" /> Import
          </button>
          <button className="btn btn-ghost" onClick={onExport}>
            <Download className="h-4 w-4" /> Export
          </button>
          <button
            className="btn btn-ghost"
            onClick={() => {
              clearAll();
              setMsg("All keys cleared from this browser.");
            }}
          >
            <Trash2 className="h-4 w-4" /> Clear all
          </button>
          <div className="ml-auto">
            <button className="btn btn-primary" onClick={onClose}>
              Done
            </button>
          </div>
          <input
            ref={fileRef}
            type="file"
            accept="application/json,.json"
            className="hidden"
            onChange={onImportFile}
          />
        </div>

        {msg && (
          <p className="mt-3 text-xs" style={{ color: "var(--muted)" }}>
            {msg}
          </p>
        )}
      </div>
    </div>
  );
}

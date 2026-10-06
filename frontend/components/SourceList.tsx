"use client";

import { ExternalLink } from "lucide-react";

import type { Source } from "@/lib/types";

function hostname(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, "");
  } catch {
    return url;
  }
}

export function SourceList({ sources }: { sources: Source[] }) {
  if (!sources?.length) return null;
  return (
    <ul className="space-y-2">
      {sources.map((s, i) => (
        <li key={`${s.url}-${i}`} className="text-sm">
          <a
            href={s.url}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1 font-medium"
            style={{ color: "var(--accent)" }}
          >
            {s.title || s.url}
            <ExternalLink className="h-3 w-3 shrink-0" />
          </a>
          {s.snippet && (
            <p className="mt-0.5 line-clamp-2" style={{ color: "var(--muted)" }}>
              {s.snippet}
            </p>
          )}
          <p className="truncate text-xs" style={{ color: "var(--muted)" }}>
            {hostname(s.url)}
          </p>
        </li>
      ))}
    </ul>
  );
}

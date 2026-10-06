// Export a finished report to Google Docs.
//   1. copyForDocs()    -- always available; copies formatted HTML + markdown
//                          to the clipboard to paste into a Google Doc.
//   2. createGoogleDoc() -- optional; needs NEXT_PUBLIC_GOOGLE_CLIENT_ID. Uses
//                          Google Identity Services to get a token, then the Docs
//                          API to create a document and insert the report.
import type { ResearchState } from "./types";

const GOOGLE_CLIENT_ID = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID || "";
const DOCS_SCOPE = "https://www.googleapis.com/auth/documents";

export function isGoogleConfigured(): boolean {
  return Boolean(GOOGLE_CLIENT_ID);
}

export function reportTitle(state: ResearchState): string {
  const q = state.query.trim();
  return q.length > 80 ? `${q.slice(0, 77)}...` : q || "Research report";
}

export function reportToMarkdown(state: ResearchState): string {
  const lines: string[] = [];
  lines.push(`# ${reportTitle(state)}`, "");
  lines.push(
    `_Model: ${state.provider} · ${state.model || "default"} — ${new Date(
      state.finishedAt ?? Date.now(),
    ).toLocaleString()}_`,
    "",
  );
  lines.push(state.report.trim(), "");
  if (state.reportSources.length) {
    lines.push("## Sources", "");
    state.reportSources.forEach((s, i) => {
      lines.push(`${i + 1}. [${s.title || s.url}](${s.url})`);
    });
  }
  return lines.join("\n");
}

function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}

// Minimal markdown -> HTML good enough for a clipboard paste into Google Docs.
function inline(s: string): string {
  return escapeHtml(s)
    .replace(/\[([^\]]+)\]\((https?:\/\/[^)]+)\)/g, '<a href="$2">$1</a>')
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

export function reportToHtml(state: ResearchState): string {
  const md = reportToMarkdown(state);
  const out: string[] = [];
  let inList = false;
  const closeList = () => {
    if (inList) {
      out.push("</ul>");
      inList = false;
    }
  };
  for (const raw of md.split("\n")) {
    const line = raw.trimEnd();
    if (!line.trim()) {
      closeList();
      continue;
    }
    const h = /^(#{1,3})\s+(.*)$/.exec(line);
    if (h) {
      closeList();
      const level = h[1].length + 1; // # -> h2
      out.push(`<h${level}>${inline(h[2])}</h${level}>`);
      continue;
    }
    const li = /^\s*(?:[-*]|\d+\.)\s+(.*)$/.exec(line);
    if (li) {
      if (!inList) {
        out.push("<ul>");
        inList = true;
      }
      out.push(`<li>${inline(li[1])}</li>`);
      continue;
    }
    closeList();
    out.push(`<p>${inline(line)}</p>`);
  }
  closeList();
  return `<div>${out.join("\n")}</div>`;
}

export async function copyForDocs(state: ResearchState): Promise<void> {
  const html = reportToHtml(state);
  const markdown = reportToMarkdown(state);
  try {
    if (typeof ClipboardItem !== "undefined" && navigator.clipboard?.write) {
      await navigator.clipboard.write([
        new ClipboardItem({
          "text/html": new Blob([html], { type: "text/html" }),
          "text/plain": new Blob([markdown], { type: "text/plain" }),
        }),
      ]);
      return;
    }
  } catch {
    /* fall through to plain text */
  }
  await navigator.clipboard.writeText(markdown);
}

// --- OAuth create-doc path ---

let gisLoaded: Promise<void> | null = null;

function loadGis(): Promise<void> {
  if (typeof window === "undefined") return Promise.reject(new Error("no window"));
  if ((window as any).google?.accounts?.oauth2) return Promise.resolve();
  if (gisLoaded) return gisLoaded;
  gisLoaded = new Promise((resolve, reject) => {
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.defer = true;
    script.onload = () => resolve();
    script.onerror = () => reject(new Error("Failed to load Google Identity Services"));
    document.head.appendChild(script);
  });
  return gisLoaded;
}

function requestAccessToken(): Promise<string> {
  return new Promise((resolve, reject) => {
    const google = (window as any).google;
    const tokenClient = google.accounts.oauth2.initTokenClient({
      client_id: GOOGLE_CLIENT_ID,
      scope: DOCS_SCOPE,
      callback: (resp: any) => {
        if (resp?.access_token) resolve(resp.access_token);
        else reject(new Error(resp?.error || "Authorization failed"));
      },
    });
    tokenClient.requestAccessToken({ prompt: "" });
  });
}

/** Creates a Google Doc with the report and returns its editable URL. */
export async function createGoogleDoc(state: ResearchState): Promise<string> {
  if (!isGoogleConfigured()) {
    throw new Error("Google export is not configured (set NEXT_PUBLIC_GOOGLE_CLIENT_ID).");
  }
  await loadGis();
  const token = await requestAccessToken();

  const createRes = await fetch("https://docs.googleapis.com/v1/documents", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    body: JSON.stringify({ title: reportTitle(state) }),
  });
  if (!createRes.ok) throw new Error(`Could not create document (${createRes.status}).`);
  const doc = await createRes.json();
  const documentId = doc.documentId as string;

  const text = reportToMarkdown(state);
  const updateRes = await fetch(
    `https://docs.googleapis.com/v1/documents/${documentId}:batchUpdate`,
    {
      method: "POST",
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
      body: JSON.stringify({
        requests: [{ insertText: { location: { index: 1 }, text } }],
      }),
    },
  );
  if (!updateRes.ok) throw new Error(`Could not write document body (${updateRes.status}).`);

  return `https://docs.google.com/document/d/${documentId}/edit`;
}

// Pure reducer: fold a ResearchEvent into a ResearchState. Shared by the main
// research view and each compare column so behaviour is identical.
import type { Finding, Provider, ResearchEvent, ResearchState, Source } from "./types";

export function initialResearchState(
  overrides: Partial<ResearchState> = {},
): ResearchState {
  return {
    id: null,
    query: "",
    provider: "openai",
    model: "",
    stage: "idle",
    statusMessage: "",
    progress: 0,
    plan: [],
    findings: [],
    report: "",
    reportSources: [],
    error: null,
    startedAt: null,
    finishedAt: null,
    running: false,
    ...overrides,
  };
}

export function applyEvent(state: ResearchState, e: ResearchEvent): ResearchState {
  const next: ResearchState = { ...state };
  if (e.research_id && !next.id) next.id = e.research_id;
  if (!next.startedAt) next.startedAt = Date.now();

  switch (e.type) {
    case "status": {
      if (e.stage) next.stage = e.stage as ResearchState["stage"];
      if (e.message) next.statusMessage = e.message;
      const p = e.data?.progress;
      if (typeof p === "number") next.progress = p;
      next.running = true;
      break;
    }
    case "plan": {
      next.stage = "planning";
      next.plan = (e.data?.subquestions as string[]) ?? [];
      break;
    }
    case "sources": {
      next.stage = "researching";
      const idx = e.data?.index as number;
      const sources = (e.data?.sources as Source[]) ?? [];
      next.findings = upsertFinding(next.findings, {
        index: idx,
        subquestion: (e.data?.subquestion as string) ?? "",
        summary: findingAt(next.findings, idx)?.summary ?? "",
        sources,
      });
      break;
    }
    case "finding": {
      next.stage = "researching";
      const idx = e.data?.index as number;
      next.findings = upsertFinding(next.findings, {
        index: idx,
        subquestion: (e.data?.subquestion as string) ?? "",
        summary: (e.data?.summary as string) ?? "",
        sources: (e.data?.sources as Source[]) ?? findingAt(next.findings, idx)?.sources ?? [],
      });
      break;
    }
    case "token": {
      next.stage = "report";
      next.report += (e.data?.text as string) ?? "";
      break;
    }
    case "report": {
      next.stage = "report";
      next.report = (e.data?.report as string) ?? next.report;
      next.reportSources = (e.data?.sources as Source[]) ?? [];
      break;
    }
    case "done": {
      next.stage = "done";
      next.running = false;
      next.finishedAt = Date.now();
      next.progress = 1;
      break;
    }
    case "error": {
      next.stage = "error";
      next.error = e.message ?? "Unknown error";
      next.running = false;
      next.finishedAt = Date.now();
      break;
    }
  }
  return next;
}

function findingAt(findings: Finding[], index: number): Finding | undefined {
  return findings.find((f) => f.index === index);
}

function upsertFinding(findings: Finding[], f: Finding): Finding[] {
  const i = findings.findIndex((x) => x.index === f.index);
  if (i === -1) return [...findings, f].sort((a, b) => a.index - b.index);
  const copy = [...findings];
  copy[i] = { ...copy[i], ...f };
  return copy;
}

export function elapsedMs(state: ResearchState): number | null {
  if (!state.startedAt) return null;
  return (state.finishedAt ?? Date.now()) - state.startedAt;
}

export function newRunState(query: string, provider: Provider, model: string): ResearchState {
  return initialResearchState({
    query,
    provider,
    model,
    stage: "planning",
    statusMessage: "Starting...",
    running: true,
    startedAt: Date.now(),
  });
}

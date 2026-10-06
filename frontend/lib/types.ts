// Mirrors ../_shared/api-contract.md. Keep in sync with backend app/models/research.py.

export type Provider = "openai" | "anthropic" | "kimi";

export interface Source {
  title: string;
  url: string;
  snippet: string;
}

export type EventType =
  | "status"
  | "plan"
  | "sources"
  | "finding"
  | "token"
  | "report"
  | "done"
  | "error";

export interface ResearchEvent {
  type: EventType;
  stage?: string | null;
  message?: string | null;
  data?: Record<string, any> | null;
  research_id: string;
  timestamp: string;
}

export interface Finding {
  index: number;
  subquestion: string;
  summary: string;
  sources: Source[];
}

export type Stage =
  | "idle"
  | "planning"
  | "researching"
  | "report"
  | "done"
  | "error";

export interface ResearchState {
  id: string | null;
  query: string;
  provider: Provider;
  model: string;
  stage: Stage;
  statusMessage: string;
  progress: number; // 0..1
  plan: string[];
  findings: Finding[];
  report: string;
  reportSources: Source[];
  error: string | null;
  startedAt: number | null;
  finishedAt: number | null;
  running: boolean;
}

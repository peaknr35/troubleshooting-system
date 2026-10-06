// Mirrors ../_shared/agent-turn-contract.md. Keep in sync with backend app/models/chat.py.
import type { Provider } from "./types";

export type TurnEventType =
  | "phase" | "thought" | "tool_call" | "tool_result"
  | "memory" | "token" | "final" | "error" | "done";

export interface TurnEvent {
  type: TurnEventType;
  phase?: string | null;
  name?: string | null;
  message?: string | null;
  data?: Record<string, any> | null;
  turn_id: string;
  timestamp: string;
}

export interface ToolActivity {
  name: string;
  args?: any;
  result?: string;
  ok?: boolean;
  running: boolean;
}

export interface TurnActivity {
  phase: string;
  phases: string[];
  tools: ToolActivity[];
  recalled: string[];
  saved: string[];
  running: boolean;
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
  activity?: TurnActivity;
}

export function emptyActivity(): TurnActivity {
  return { phase: "receive", phases: [], tools: [], recalled: [], saved: [], running: true };
}

export interface MemoryFact { id: number; text: string; kind: string; source: string; created_at: string; }
export interface ToolRun { turn_id: number | null; tool: string; args: string; result: string; ok: number; created_at: string; }

export type { Provider };

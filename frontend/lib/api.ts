// SSE client. We POST the request (so EventSource is unusable) and parse the
// text/event-stream body manually from a fetch ReadableStream.
import type { Provider, ResearchEvent } from "./types";

export const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL?.replace(/\/$/, "") || "http://localhost:8080";

export interface StreamParams {
  query: string;
  provider: Provider;
  model: string;
  apiKey: string;
  maxSubquestions?: number;
  search?: boolean;
  signal?: AbortSignal;
}

function errorEvent(message: string, code = "internal"): ResearchEvent {
  return {
    type: "error",
    stage: "error",
    message,
    data: { code },
    research_id: "",
    timestamp: new Date().toISOString(),
  };
}

/**
 * Stream a research run. Calls onEvent for every parsed SSE event. Resolves when
 * the stream ends. Network/validation problems are delivered as an `error` event
 * (not thrown), so callers only need one code path.
 */
export async function streamResearch(
  params: StreamParams,
  onEvent: (e: ResearchEvent) => void,
): Promise<void> {
  let res: Response;
  try {
    res = await fetch(`${BACKEND_URL}/research/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        query: params.query,
        provider: params.provider,
        model: params.model || undefined,
        api_key: params.apiKey,
        max_subquestions: params.maxSubquestions ?? 4,
        search: params.search ?? true,
      }),
      signal: params.signal,
    });
  } catch (err: any) {
    if (err?.name === "AbortError") return;
    onEvent(errorEvent(`Could not reach the backend at ${BACKEND_URL}.`, "network"));
    return;
  }

  if (!res.ok || !res.body) {
    let msg = `Request failed (${res.status}).`;
    try {
      const body = await res.json();
      if (body?.detail) {
        msg =
          typeof body.detail === "string"
            ? body.detail
            : body.detail?.[0]?.msg
              ? `Invalid request: ${body.detail[0].msg}`
              : JSON.stringify(body.detail);
      }
    } catch {
      /* non-JSON body */
    }
    onEvent(errorEvent(msg, res.status === 422 ? "validation" : "provider"));
    return;
  }

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });

      let sep: number;
      while ((sep = buffer.indexOf("\n\n")) >= 0) {
        const frame = buffer.slice(0, sep);
        buffer = buffer.slice(sep + 2);
        for (const line of frame.split("\n")) {
          const trimmed = line.trimStart();
          if (!trimmed.startsWith("data:")) continue;
          const payload = trimmed.slice(5).trim();
          if (!payload) continue;
          try {
            onEvent(JSON.parse(payload) as ResearchEvent);
          } catch {
            /* ignore malformed frame */
          }
        }
      }
    }
  } catch (err: any) {
    if (err?.name !== "AbortError") {
      onEvent(errorEvent("The stream was interrupted.", "network"));
    }
  }
}

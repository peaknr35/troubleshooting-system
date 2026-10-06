// Browser-only persistence for API keys. Keys never leave the browser except as
// the per-request body to our backend, which forwards them to the chosen provider.
import type { Provider } from "./types";

const KEYS_STORAGE = "drs.apiKeys.v1";

export type ApiKeys = Partial<Record<Provider, string>>;

export function loadKeys(): ApiKeys {
  if (typeof window === "undefined") return {};
  try {
    const raw = window.localStorage.getItem(KEYS_STORAGE);
    return raw ? (JSON.parse(raw) as ApiKeys) : {};
  } catch {
    return {};
  }
}

export function saveKeys(keys: ApiKeys): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.setItem(KEYS_STORAGE, JSON.stringify(keys));
  } catch {
    /* storage full / blocked: ignore, in-memory state still works */
  }
}

export function clearKeys(): void {
  if (typeof window === "undefined") return;
  try {
    window.localStorage.removeItem(KEYS_STORAGE);
  } catch {
    /* ignore */
  }
}

export function exportKeysJson(keys: ApiKeys): string {
  return JSON.stringify(keys, null, 2);
}

export function parseKeysJson(json: string): ApiKeys {
  const data = JSON.parse(json);
  const out: ApiKeys = {};
  for (const p of ["openai", "anthropic", "kimi"] as Provider[]) {
    if (typeof data?.[p] === "string" && data[p].trim()) out[p] = data[p].trim();
  }
  return out;
}

// Generic session-scoped state persistence (survives route changes and reloads
// within a tab). Used to keep research results when navigating around.
export function loadSession<T>(key: string, fallback: T): T {
  if (typeof window === "undefined") return fallback;
  try {
    const raw = window.sessionStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

export function saveSession<T>(key: string, value: T): void {
  if (typeof window === "undefined") return;
  try {
    window.sessionStorage.setItem(key, JSON.stringify(value));
  } catch {
    /* ignore */
  }
}

"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

import {
  type ApiKeys,
  clearKeys,
  exportKeysJson,
  loadKeys,
  parseKeysJson,
  saveKeys,
} from "@/lib/storage";
import type { Provider } from "@/lib/types";

interface ApiKeyContextValue {
  keys: ApiKeys;
  hydrated: boolean;
  setKey: (provider: Provider, value: string) => void;
  removeKey: (provider: Provider) => void;
  clearAll: () => void;
  hasKey: (provider: Provider) => boolean;
  importFromJson: (json: string) => void; // throws on invalid JSON
  exportJson: () => string;
}

const ApiKeyContext = createContext<ApiKeyContextValue | null>(null);

export function ApiKeyProvider({ children }: { children: ReactNode }) {
  const [keys, setKeys] = useState<ApiKeys>({});
  const [hydrated, setHydrated] = useState(false);

  useEffect(() => {
    setKeys(loadKeys());
    setHydrated(true);
  }, []);

  useEffect(() => {
    if (hydrated) saveKeys(keys);
  }, [keys, hydrated]);

  const value: ApiKeyContextValue = {
    keys,
    hydrated,
    setKey: (provider, v) => setKeys((k) => ({ ...k, [provider]: v })),
    removeKey: (provider) =>
      setKeys((k) => {
        const next = { ...k };
        delete next[provider];
        return next;
      }),
    clearAll: () => {
      setKeys({});
      clearKeys();
    },
    hasKey: (provider) => Boolean(keys[provider] && keys[provider]!.trim()),
    importFromJson: (json) => setKeys((prev) => ({ ...prev, ...parseKeysJson(json) })),
    exportJson: () => exportKeysJson(keys),
  };

  return <ApiKeyContext.Provider value={value}>{children}</ApiKeyContext.Provider>;
}

export function useApiKeys(): ApiKeyContextValue {
  const ctx = useContext(ApiKeyContext);
  if (!ctx) throw new Error("useApiKeys must be used within <ApiKeyProvider>");
  return ctx;
}

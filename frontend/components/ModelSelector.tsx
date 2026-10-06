"use client";

import { useApiKeys } from "@/contexts/ApiKeyContext";
import { PROVIDERS, providerById } from "@/lib/models";
import type { Provider } from "@/lib/types";

export function ModelSelector({
  provider,
  model,
  onChange,
}: {
  provider: Provider;
  model: string;
  onChange: (provider: Provider, model: string) => void;
}) {
  const { hasKey } = useApiKeys();
  const info = providerById(provider);
  const keyed = hasKey(provider);

  return (
    <div className="flex flex-wrap items-center gap-2">
      <select
        className="input !w-auto"
        value={provider}
        onChange={(e) => {
          const np = e.target.value as Provider;
          onChange(np, providerById(np).defaultModel);
        }}
        aria-label="Provider"
      >
        {PROVIDERS.map((p) => (
          <option key={p.id} value={p.id}>
            {p.label}
          </option>
        ))}
      </select>
      <select
        className="input !w-auto"
        value={model}
        onChange={(e) => onChange(provider, e.target.value)}
        aria-label="Model"
      >
        {info.models.map((m) => (
          <option key={m} value={m}>
            {m}
          </option>
        ))}
      </select>
      <span className="chip" title={keyed ? "Key set for this provider" : "No key saved for this provider"}>
        <span
          className="h-2 w-2 rounded-full"
          style={{ background: keyed ? "#38b36b" : "#d4a017" }}
        />
        {keyed ? "key set" : "no key"}
      </span>
    </div>
  );
}

"use client";

import type { ReactNode } from "react";

import { Header } from "@/components/Header";
import { ApiKeyProvider } from "@/contexts/ApiKeyContext";
import { ResearchProvider } from "@/contexts/ResearchContext";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ApiKeyProvider>
      <ResearchProvider>
        <Header />
        {children}
      </ResearchProvider>
    </ApiKeyProvider>
  );
}

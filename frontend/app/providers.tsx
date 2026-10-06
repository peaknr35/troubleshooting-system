"use client";

import type { ReactNode } from "react";

import { Header } from "@/components/Header";
import { ApiKeyProvider } from "@/contexts/ApiKeyContext";
import { ChatProvider } from "@/contexts/ChatContext";
import { ResearchProvider } from "@/contexts/ResearchContext";

export function Providers({ children }: { children: ReactNode }) {
  return (
    <ApiKeyProvider>
      <ChatProvider>
        <ResearchProvider>
          <Header />
          {children}
        </ResearchProvider>
      </ChatProvider>
    </ApiKeyProvider>
  );
}

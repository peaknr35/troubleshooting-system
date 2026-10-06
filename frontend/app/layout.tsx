import type { Metadata } from "next";

import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Deep Research Studio",
  description:
    "Ask a question and watch a real research workflow run live across OpenAI, Anthropic, and Kimi K2. Bring your own key.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}

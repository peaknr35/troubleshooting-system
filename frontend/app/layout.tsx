import type { Metadata } from "next";

import "./globals.css";
import { Providers } from "./providers";

export const metadata: Metadata = {
  title: "Local Agent",
  description:
    "A local-first personal AI assistant: chat in the terminal or browser, one SQLite brain, tools for real work. Deep Research Studio is one of its tools. Bring your own key.",
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

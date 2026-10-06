"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { FlaskConical, GitCompare, Home, KeyRound } from "lucide-react";

import { ApiKeyManager } from "./ApiKeyManager";

const NAV = [
  { href: "/", label: "Research", icon: Home },
  { href: "/compare", label: "Compare", icon: GitCompare },
];

export function Header() {
  const [keysOpen, setKeysOpen] = useState(false);
  const pathname = usePathname();

  return (
    <>
      <header
        className="sticky top-0 z-20 border-b backdrop-blur"
        style={{
          borderColor: "var(--border)",
          background: "color-mix(in srgb, var(--bg) 85%, transparent)",
        }}
      >
        <div className="mx-auto flex max-w-6xl items-center justify-between gap-3 px-4 py-3">
          <Link href="/" className="flex items-center gap-2 font-semibold">
            <FlaskConical className="h-5 w-5" style={{ color: "var(--accent)" }} />
            <span>Deep Research Studio</span>
          </Link>
          <nav className="flex items-center gap-1">
            {NAV.map((n) => {
              const active = pathname === n.href;
              const Icon = n.icon;
              return (
                <Link
                  key={n.href}
                  href={n.href}
                  className="btn btn-ghost"
                  style={active ? { background: "var(--surface-2)" } : undefined}
                >
                  <Icon className="h-4 w-4" />
                  <span className="hidden sm:inline">{n.label}</span>
                </Link>
              );
            })}
            <button className="btn btn-ghost" onClick={() => setKeysOpen(true)}>
              <KeyRound className="h-4 w-4" />
              <span className="hidden sm:inline">Keys</span>
            </button>
          </nav>
        </div>
      </header>
      <ApiKeyManager open={keysOpen} onClose={() => setKeysOpen(false)} />
    </>
  );
}

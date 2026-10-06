"use client";

const COLORS: Record<string, string> = {
  receive: "#8b7dff", recall: "#4aa3ff", reason: "#d4a017", act: "#e08a3c",
  observe: "#38b36b", remember: "#c266d9", reply: "#38b36b", done: "#6b6b76", error: "#d9534f",
};

export function PhaseBadge({ phase, active }: { phase: string; active?: boolean }) {
  const c = COLORS[phase] ?? "#6b6b76";
  return (
    <span
      className="inline-flex items-center gap-1 rounded-full px-2 py-0.5 text-xs"
      style={{ background: `${c}22`, color: c, border: `1px solid ${c}55` }}
    >
      {active && <span className="pulse-dot h-1.5 w-1.5 rounded-full" style={{ background: c }} />}
      {phase}
    </span>
  );
}

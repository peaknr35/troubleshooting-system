"use client";

import type { TurnActivity } from "@/lib/chatTypes";
import { PhaseBadge } from "./PhaseBadge";
import { ToolCallCard } from "./ToolCallCard";

export function TurnTimeline({ activity }: { activity: TurnActivity }) {
  return (
    <div className="space-y-2">
      <div className="flex flex-wrap items-center gap-1.5">
        {activity.phases.map((p, i) => (
          <PhaseBadge key={i} phase={p} active={activity.running && p === activity.phase} />
        ))}
      </div>
      {activity.recalled.length > 0 && (
        <div className="text-xs" style={{ color: "var(--muted)" }}>
          recalled: {activity.recalled.join("  .  ")}
        </div>
      )}
      {activity.tools.length > 0 && (
        <div className="space-y-1.5">
          {activity.tools.map((t, i) => <ToolCallCard key={i} tool={t} />)}
        </div>
      )}
      {activity.saved.length > 0 && (
        <div className="text-xs" style={{ color: "#c266d9" }}>
          remembered: {activity.saved.join("  .  ")}
        </div>
      )}
    </div>
  );
}

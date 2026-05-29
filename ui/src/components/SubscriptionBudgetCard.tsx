import { useMemo } from "react";
import type { QuotaWindow } from "@paperclipai/shared";
import { Gauge } from "lucide-react";
import { cn, quotaSourceDisplayName } from "@/lib/utils";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";

const WINDOW_ORDER = [
  "currentsession",
  "currentweekallmodels",
  "currentweeksonnetonly",
  "currentweeksonnet",
  "currentweekopusonly",
  "currentweekopus",
] as const;

function normalizeLabel(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, "");
}

function isExtraUsage(window: QuotaWindow): boolean {
  return normalizeLabel(window.label) === "extrausage";
}

function orderedWindows(windows: QuotaWindow[]): QuotaWindow[] {
  return windows
    .filter((w) => !isExtraUsage(w))
    .sort((a, b) => {
      const aIndex = WINDOW_ORDER.indexOf(normalizeLabel(a.label) as (typeof WINDOW_ORDER)[number]);
      const bIndex = WINDOW_ORDER.indexOf(normalizeLabel(b.label) as (typeof WINDOW_ORDER)[number]);
      return (aIndex === -1 ? WINDOW_ORDER.length : aIndex) - (bIndex === -1 ? WINDOW_ORDER.length : bIndex);
    });
}

function statusForPercent(pct: number | null): "ok" | "warning" | "critical" {
  if (pct == null) return "ok";
  if (pct >= 90) return "critical";
  if (pct >= 70) return "warning";
  return "ok";
}

function fillClass(status: "ok" | "warning" | "critical"): string {
  if (status === "critical") return "bg-red-400";
  if (status === "warning") return "bg-amber-300";
  return "bg-emerald-300";
}

function statusTone(status: "ok" | "warning" | "critical"): string {
  if (status === "critical") return "text-red-300 border-red-500/30 bg-red-500/10";
  if (status === "warning") return "text-amber-200 border-amber-500/30 bg-amber-500/10";
  return "text-emerald-200 border-emerald-500/30 bg-emerald-500/10";
}

function formatResetTime(resetsAt: string | null): string | null {
  if (!resetsAt) return null;
  const formatted = new Date(resetsAt).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  });
  return `Resets ${formatted}`;
}

interface SubscriptionBudgetCardProps {
  quotaWindows: QuotaWindow[];
  source?: string | null;
  error?: string | null;
  loading?: boolean;
}

export function SubscriptionBudgetCard({
  quotaWindows,
  source = null,
  error = null,
  loading = false,
}: SubscriptionBudgetCardProps) {
  const ordered = useMemo(() => orderedWindows(quotaWindows), [quotaWindows]);

  const overallStatus = useMemo(() => {
    let worst: "ok" | "warning" | "critical" = "ok";
    for (const w of ordered) {
      const s = statusForPercent(w.usedPercent);
      if (s === "critical") return "critical";
      if (s === "warning") worst = "warning";
    }
    return worst;
  }, [ordered]);

  if (loading) {
    return (
      <Card className="overflow-hidden border-border/70 bg-card/80 shadow-[0_20px_80px_-40px_rgba(0,0,0,0.55)]">
        <CardHeader className="px-5 pt-5 pb-3">
          <Skeleton className="h-4 w-48" />
          <Skeleton className="mt-2 h-3 w-64" />
        </CardHeader>
        <CardContent className="space-y-4 px-5 pb-5 pt-0">
          {Array.from({ length: 3 }).map((_, i) => (
            <div key={i} className="space-y-2">
              <Skeleton className="h-3 w-40" />
              <Skeleton className="h-2 w-full" />
            </div>
          ))}
        </CardContent>
      </Card>
    );
  }

  if (ordered.length === 0 && !error) return null;

  return (
    <Card className="overflow-hidden border-border/70 bg-card/80 shadow-[0_20px_80px_-40px_rgba(0,0,0,0.55)]">
      <CardHeader className="px-5 pt-5 pb-3">
        <div className="flex items-start justify-between gap-3">
          <div>
            <div className="text-[11px] uppercase tracking-[0.22em] text-muted-foreground">
              subscription
            </div>
            <CardTitle className="mt-1 text-base">Anthropic subscription quota</CardTitle>
            <CardDescription className="mt-1">
              Live session and weekly usage limits from your Claude subscription.
            </CardDescription>
          </div>
          <div className="flex items-center gap-2">
            {source ? (
              <span className="shrink-0 border border-border px-2.5 py-1 text-[10px] font-semibold uppercase tracking-[0.16em] text-muted-foreground">
                {quotaSourceDisplayName(source)}
              </span>
            ) : null}
            <div className={cn("inline-flex items-center gap-2 rounded-full border px-3 py-1 text-[11px] uppercase tracking-[0.18em]", statusTone(overallStatus))}>
              <Gauge className="h-3.5 w-3.5" />
              {overallStatus === "critical" ? "Near limit" : overallStatus === "warning" ? "Warning" : "Healthy"}
            </div>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4 px-5 pb-5 pt-0">
        {error ? (
          <div className="rounded-xl border border-destructive/40 bg-destructive/10 px-3 py-2 text-sm text-destructive">
            {error}
          </div>
        ) : null}

        {/* observed/budget-style grid for the highest utilization window */}
        {ordered.length > 0 && (() => {
          const primary = ordered.reduce((max, w) =>
            (w.usedPercent ?? 0) > (max.usedPercent ?? 0) ? w : max, ordered[0]!);
          const pct = primary.usedPercent ?? 0;
          const remaining = Math.max(0, 100 - pct);
          return (
            <div className="grid gap-3 sm:grid-cols-2">
              <div className="rounded-xl border border-border/70 bg-black/[0.18] px-4 py-3">
                <div className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">Used</div>
                <div className="mt-2 text-xl font-semibold tabular-nums">{pct}%</div>
                <div className="mt-1 text-xs text-muted-foreground">
                  {primary.label}
                </div>
              </div>
              <div className="rounded-xl border border-border/70 bg-black/[0.18] px-4 py-3">
                <div className="text-[11px] uppercase tracking-[0.18em] text-muted-foreground">Remaining</div>
                <div className="mt-2 text-xl font-semibold tabular-nums">{remaining}%</div>
                <div className="mt-1 text-xs text-muted-foreground">
                  {formatResetTime(primary.resetsAt) ?? "Managed by Anthropic"}
                </div>
              </div>
            </div>
          );
        })()}

        {/* progress bars for each window */}
        {ordered.map((window) => {
          const pct = Math.min(100, Math.max(0, window.usedPercent ?? 0));
          const status = statusForPercent(window.usedPercent);
          const resetText = window.detail ?? formatResetTime(window.resetsAt);
          return (
            <div key={window.label} className="space-y-2">
              <div className="flex items-center justify-between gap-2">
                <span className="text-sm font-medium text-foreground">{window.label}</span>
                {window.usedPercent != null ? (
                  <span className="text-sm font-semibold tabular-nums text-foreground">{window.usedPercent}% used</span>
                ) : null}
              </div>
              <div className="h-2 overflow-hidden rounded-full bg-muted/70">
                <div
                  className={cn("h-full rounded-full transition-[width,background-color] duration-200", fillClass(status))}
                  style={{ width: `${pct}%` }}
                />
              </div>
              {resetText ? (
                <p className="text-xs text-muted-foreground">{resetText}</p>
              ) : null}
            </div>
          );
        })}
      </CardContent>
    </Card>
  );
}

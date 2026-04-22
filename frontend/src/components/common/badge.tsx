import { cn } from "@/lib/utils";

export function Badge({ children, className }: { children: string; className?: string }) {
  return (
    <span className={cn("inline-flex rounded-full border border-gold/20 bg-gold/10 px-3 py-1 text-xs font-semibold uppercase tracking-[0.22em] text-charcoal/80", className)}>
      {children}
    </span>
  );
}

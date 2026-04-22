import type { PropsWithChildren } from "react";

import { cn } from "@/lib/utils";

export function Card({ children, className }: PropsWithChildren<{ className?: string }>) {
  return (
    <div className={cn("rounded-[2rem] border border-charcoal/10 bg-white/75 p-6 shadow-halo backdrop-blur-sm", className)}>
      {children}
    </div>
  );
}

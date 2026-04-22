import type { PropsWithChildren } from "react";

export function SectionShell({ children, id }: PropsWithChildren<{ id?: string }>) {
  return <section id={id} className="mx-auto max-w-7xl px-6 py-20">{children}</section>;
}

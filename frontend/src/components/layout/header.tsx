import { Link } from "react-router-dom";

import { Button } from "@/components/common/button";

export function Header() {
  return (
    <header className="sticky top-0 z-20 border-b border-charcoal/5 bg-ivory/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link to="/" className="font-display text-3xl tracking-[0.15em] text-charcoal">
          Aurelium
        </Link>
        <nav className="hidden items-center gap-8 md:flex">
          <a href="#craft" className="text-sm text-charcoal/70 transition hover:text-charcoal">Craft</a>
          <a href="#categories" className="text-sm text-charcoal/70 transition hover:text-charcoal">Collections</a>
          <a href="#trust" className="text-sm text-charcoal/70 transition hover:text-charcoal">Realism</a>
        </nav>
        <Button asChild variant="secondary">
          <Link to="/studio">Begin preview</Link>
        </Button>
      </div>
    </header>
  );
}

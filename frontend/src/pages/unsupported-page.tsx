import { Link } from "react-router-dom";

import { Button } from "@/components/common/button";
import { Card } from "@/components/common/card";
import { Header } from "@/components/layout/header";

export function UnsupportedPage() {
  return (
    <div className="min-h-screen bg-ivory text-charcoal">
      <Header />
      <main className="mx-auto flex max-w-3xl px-6 py-20">
        <Card className="w-full bg-white/80 p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.22em] text-charcoal/55">Portrait not suitable yet</p>
          <h1 className="mt-4 font-display text-5xl">This image needs a clearer consultation view.</h1>
          <p className="mt-4 text-sm leading-7 text-charcoal/72">
            Please upload a portrait with one person, a clearly visible face, and a visible neckline or hand depending on the jewellery category you want to preview.
          </p>
          <Button asChild className="mt-8">
            <Link to="/studio">Try another portrait</Link>
          </Button>
        </Card>
      </main>
    </div>
  );
}

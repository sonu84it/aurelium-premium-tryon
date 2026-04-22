import { ChevronRight } from "lucide-react";
import { Link } from "react-router-dom";

import { HeroSection } from "@/components/hero/hero-section";

export function LandingPage() {
  return (
    <div className="min-h-screen bg-zinc-950 font-sans text-zinc-50 antialiased selection:bg-amber-200/30">
      <nav className="sticky top-0 z-50 flex w-full justify-center border-b border-zinc-900/70 bg-zinc-950/80 p-5 backdrop-blur">
        <h1 className="font-serif text-lg uppercase tracking-[0.3em] text-zinc-100 md:text-xl">Aurelium</h1>
      </nav>
      <HeroSection />
      <div className="relative z-10 px-4 pb-10 md:px-6 md:pb-14">
        <div className="mx-auto flex w-full max-w-4xl flex-col items-center rounded-[2rem] border border-zinc-800 bg-zinc-900/80 px-6 py-6 text-center shadow-2xl backdrop-blur md:flex-row md:justify-between md:px-8">
          <div className="max-w-2xl">
            <p className="text-xs uppercase tracking-[0.22em] text-amber-200/80">Start With One Portrait</p>
            <p className="mt-3 text-sm leading-7 text-zinc-400 md:text-base">
              Upload your image, choose the jewellery category you want to explore, select a style direction, and generate curated premium looks in the final step.
            </p>
          </div>
          <Link
            to="/studio"
            className="group mt-5 inline-flex items-center gap-3 rounded-full bg-zinc-100 px-7 py-4 text-zinc-900 transition-all duration-500 hover:bg-amber-50 md:mt-0"
          >
            <span className="text-sm font-medium uppercase tracking-widest">Begin Consultation</span>
            <ChevronRight size={16} className="transition-transform group-hover:translate-x-1" />
          </Link>
        </div>
      </div>
      <div className="px-4 pb-14 md:px-6">
        <div className="mx-auto grid w-full max-w-6xl gap-4 md:grid-cols-3">
          <div className="rounded-[1.8rem] border border-zinc-800 bg-zinc-900/55 p-6">
            <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Upload</p>
            <p className="mt-3 font-serif text-2xl text-zinc-100">Share a clear portrait</p>
            <p className="mt-3 text-sm leading-7 text-zinc-400">One person only, with a clear face. Visible neckline helps necklaces. Visible hand helps rings.</p>
          </div>
          <div className="rounded-[1.8rem] border border-zinc-800 bg-zinc-900/55 p-6">
            <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Select</p>
            <p className="mt-3 font-serif text-2xl text-zinc-100">Choose category and style</p>
            <p className="mt-3 text-sm leading-7 text-zinc-400">Keep the process simple with one jewellery focus and one luxury style direction.</p>
          </div>
          <div className="rounded-[1.8rem] border border-zinc-800 bg-zinc-900/55 p-6">
            <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Generate</p>
            <p className="mt-3 font-serif text-2xl text-zinc-100">Review curated looks</p>
            <p className="mt-3 text-sm leading-7 text-zinc-400">Aurelium composes premium preview variations while preserving your portrait and background.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

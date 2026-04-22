import { useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Download, MessageSquare, SlidersHorizontal, Sparkles, X } from "lucide-react";
import { Link, Navigate } from "react-router-dom";

import { useAurelium } from "@/hooks/useAurelium";
import { generatePreview, resolveAssetUrl } from "@/services/api";
import type { GenerateRequest, JewelleryType, MetalType, ScaleType, StoneType, StyleType } from "@/types";

export function ResultsPage() {
  const {
    upload,
    results,
    selectedCategory,
    selectedMetal,
    selectedStone,
    setResults,
    setSelectedMetal,
    setSelectedStone,
  } = useAurelium();
  const [activeLook, setActiveLook] = useState(0);
  const [isRefineOpen, setIsRefineOpen] = useState(false);

  if (!upload?.original_url || !results) {
    return <Navigate to="/studio" replace />;
  }

  const featured = results.results[activeLook] ?? results.results[0];
  const lookLabels = [
    { label: "The Timeless", desc: "Classic silhouette, brilliant cut." },
    { label: "The Avant-Garde", desc: "Bold geometry, unexpected lines." },
    { label: "The Romantic", desc: "Soft curves, vintage inspiration." },
  ];

  const defaults = useMemo(() => {
    const config: Record<JewelleryType, { style: StyleType; scale: ScaleType; variant: string }> = {
      earrings: { style: "signature_minimal", scale: "refined", variant: "studs" },
      necklace: { style: "evening_elegance", scale: "statement", variant: "pendant" },
      nose_pin: { style: "signature_minimal", scale: "refined", variant: "solitaire" },
      ring: { style: "contemporary_couture", scale: "statement", variant: "solitaire_ring" },
    };
    return config[selectedCategory];
  }, [selectedCategory]);

  const refineMutation = useMutation({
    mutationFn: (): Promise<Awaited<ReturnType<typeof generatePreview>>> => {
      const payload: GenerateRequest = {
        image_id: upload.image_id,
        jewelleryType: selectedCategory,
        metal: selectedMetal,
        stone: selectedStone,
        style: defaults.style,
        scale: defaults.scale,
        variant: defaults.variant,
        placement: {
          side: "left",
          finger: "ring",
        },
        variants: 3,
      };
      return generatePreview(payload);
    },
    onSuccess: (response) => {
      setResults(response);
      setActiveLook(0);
      setIsRefineOpen(false);
    },
  });

  const metals: Array<{ id: MetalType; name: string; color: string }> = [
    { id: "yellow_gold", name: "Yellow Gold", color: "bg-yellow-400" },
    { id: "white_gold", name: "White Gold", color: "bg-zinc-300" },
    { id: "rose_gold", name: "Rose Gold", color: "bg-rose-300" },
    { id: "platinum", name: "Platinum", color: "bg-slate-200" },
  ];

  const stones: Array<{ id: StoneType; name: string; color: string }> = [
    { id: "diamond", name: "Diamond", color: "bg-white" },
    { id: "emerald", name: "Emerald", color: "bg-emerald-600" },
    { id: "ruby", name: "Ruby", color: "bg-red-600" },
    { id: "sapphire", name: "Sapphire", color: "bg-blue-800" },
  ];

  return (
    <div className="min-h-screen bg-zinc-950 font-sans text-zinc-50 antialiased selection:bg-amber-200/30">
      <nav className="sticky top-0 z-20 flex w-full justify-center border-b border-zinc-900/70 bg-zinc-950/80 p-5 backdrop-blur">
        <h1 className="font-serif text-lg uppercase tracking-[0.3em] text-zinc-100 md:text-xl">Aurelium</h1>
      </nav>
      <main className="mx-auto flex w-full max-w-7xl flex-col gap-6 px-4 py-6 md:px-6 md:py-10">
        <section className="text-center">
          <p className="mb-2 text-xs uppercase tracking-[0.2em] text-amber-200/80">{selectedCategory.replace("_", " ")}</p>
          <h2 className="font-serif text-3xl text-zinc-100 md:text-5xl">{lookLabels[activeLook]?.label ?? featured.title}</h2>
          <p className="mt-3 text-sm font-light text-zinc-400 md:text-base">{lookLabels[activeLook]?.desc ?? featured.title}</p>
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
          <div className="overflow-hidden rounded-[2rem] border border-zinc-800 bg-zinc-900/60">
            <div className="grid gap-3 p-3 md:grid-cols-2">
              <div className="overflow-hidden rounded-[1.5rem] border border-zinc-800 bg-zinc-950/70">
                <div className="border-b border-zinc-800 px-4 py-3 text-xs uppercase tracking-[0.22em] text-zinc-500">Original</div>
                <img src={resolveAssetUrl(upload.original_url)} alt="Original portrait" className="aspect-[4/5] w-full object-cover" />
              </div>
              <div className="overflow-hidden rounded-[1.5rem] border border-zinc-800 bg-zinc-950/70">
                <div className="border-b border-zinc-800 px-4 py-3 text-xs uppercase tracking-[0.22em] text-zinc-500">Preview</div>
                <div className="relative">
                  <img src={resolveAssetUrl(featured.url)} alt={featured.title} className="aspect-[4/5] w-full object-cover" />
                  <div className="pointer-events-none absolute inset-0 bg-gradient-to-t from-zinc-950/35 via-transparent to-zinc-950/10" />
                  <Sparkles className="absolute right-5 top-5 animate-pulse text-amber-200/70" size={16} />
                </div>
              </div>
            </div>
          </div>

          <div className="space-y-6">
            <section className="rounded-[2rem] border border-zinc-800 bg-zinc-900/60 p-5 md:p-6">
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Curated Variations</p>
              <div className="mt-5 grid gap-3">
                {results.results.map((result, index) => (
                  <button
                    key={result.url}
                    onClick={() => setActiveLook(index)}
                    className={`rounded-[1.3rem] border px-4 py-4 text-left transition-all duration-300 ${
                      activeLook === index ? "border-amber-200/60 bg-amber-200/8" : "border-zinc-800 bg-zinc-950/40 hover:border-zinc-700"
                    }`}
                  >
                    <p className="font-serif text-xl text-zinc-100">{lookLabels[index]?.label ?? result.title}</p>
                    <p className="mt-2 text-sm leading-6 text-zinc-400">{lookLabels[index]?.desc ?? result.title}</p>
                  </button>
                ))}
              </div>
            </section>

            <section className="rounded-[2rem] border border-zinc-800 bg-zinc-900/60 p-5 md:p-6">
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Actions</p>
              <div className="mt-5 flex flex-col gap-3 sm:flex-row">
                <button
                  onClick={() => setIsRefineOpen(true)}
                  className="flex flex-1 items-center justify-center gap-2 rounded-full border border-zinc-700 px-5 py-4 text-sm uppercase tracking-widest text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-800"
                >
                  <SlidersHorizontal size={14} />
                  Refine
                </button>
                <a
                  href={resolveAssetUrl(featured.url)}
                  download
                  className="flex flex-1 items-center justify-center gap-2 rounded-full bg-zinc-100 px-5 py-4 text-sm uppercase tracking-widest text-zinc-900 transition-colors hover:bg-white"
                >
                  <Download size={14} />
                  Download
                </a>
                <Link
                  to="/studio"
                  className="flex flex-1 items-center justify-center gap-2 rounded-full border border-zinc-700 px-5 py-4 text-sm uppercase tracking-widest text-zinc-200 transition-colors hover:border-zinc-600 hover:bg-zinc-800"
                >
                  <MessageSquare size={14} />
                  Try Another
                </Link>
              </div>
            </section>
          </div>
        </section>
      </main>

      {isRefineOpen ? (
        <>
          <div className="absolute inset-0 z-30 bg-zinc-950/60 backdrop-blur-sm animate-in fade-in duration-300" onClick={() => setIsRefineOpen(false)} />
          <div className="fixed bottom-0 left-0 z-40 w-full rounded-t-3xl border-t border-zinc-800 bg-zinc-900 p-6 md:p-8 animate-in slide-in-from-bottom-full duration-500">
            <div className="mb-8 flex items-center justify-between">
              <h3 className="font-serif text-xl text-zinc-100">Refine Collection</h3>
              <button onClick={() => setIsRefineOpen(false)} className="rounded-full p-2 text-zinc-500 transition-colors hover:bg-zinc-800 hover:text-zinc-300">
                <X size={20} />
              </button>
            </div>

            <div className="space-y-8">
              <div>
                <p className="mb-4 text-xs uppercase tracking-widest text-zinc-500">Material</p>
                <div className="scrollbar-hide flex gap-4 overflow-x-auto pb-2">
                  {metals.map((item) => (
                    <button key={item.id} onClick={() => setSelectedMetal(item.id)} className="group flex flex-shrink-0 flex-col items-center gap-2">
                      <div className={`h-12 w-12 rounded-full border-2 transition-all duration-300 ${selectedMetal === item.id ? "border-amber-200 p-1" : "border-transparent"}`}>
                        <div className={`h-full w-full rounded-full ${item.color} shadow-inner opacity-80`} />
                      </div>
                      <span className={`text-[10px] uppercase tracking-widest ${selectedMetal === item.id ? "text-zinc-300" : "text-zinc-600 group-hover:text-zinc-400"}`}>
                        {item.name}
                      </span>
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <p className="mb-4 text-xs uppercase tracking-widest text-zinc-500">Primary Stone</p>
                <div className="scrollbar-hide flex gap-4 overflow-x-auto pb-2">
                  {stones.map((item) => (
                    <button key={item.id} onClick={() => setSelectedStone(item.id)} className="group flex flex-shrink-0 flex-col items-center gap-2">
                      <div className={`h-12 w-12 rounded-full border-2 transition-all duration-300 ${selectedStone === item.id ? "border-amber-200 p-1" : "border-transparent"}`}>
                        <div className={`h-full w-full rounded-full ${item.color} shadow-inner opacity-90`} />
                      </div>
                      <span className={`text-[10px] uppercase tracking-widest ${selectedStone === item.id ? "text-zinc-300" : "text-zinc-600 group-hover:text-zinc-400"}`}>
                        {item.name}
                      </span>
                    </button>
                  ))}
                </div>
              </div>
            </div>

            <button
              onClick={() => refineMutation.mutate()}
              disabled={refineMutation.isPending}
              className="mt-10 w-full rounded-full bg-zinc-100 py-4 text-xs font-bold uppercase tracking-widest text-zinc-900 transition-colors hover:bg-white disabled:opacity-60"
            >
              {refineMutation.isPending ? "Applying Curation" : "Apply Curation"}
            </button>
          </div>
        </>
      ) : null}
    </div>
  );
}

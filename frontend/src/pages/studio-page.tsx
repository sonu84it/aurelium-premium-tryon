import { useMemo, useState } from "react";
import { useMutation } from "@tanstack/react-query";
import { Link, useNavigate } from "react-router-dom";
import { Camera, ChevronRight, Gem, Sparkles, Circle, ShieldCheck, ScanFace } from "lucide-react";

import { useAurelium } from "@/hooks/useAurelium";
import { analyzePortrait, generatePreview, resolveAssetUrl, uploadPortrait } from "@/services/api";
import type { GenerateRequest, JewelleryType, ScaleType, StyleType } from "@/types";

export function StudioPage() {
  const navigate = useNavigate();
  const {
    upload,
    analysis,
    setUpload,
    setAnalysis,
    setResults,
    selectedCategory,
    setSelectedCategory,
    selectedMetal,
    selectedStone,
  } = useAurelium();

  const [previewUrl, setPreviewUrl] = useState<string | undefined>(upload?.original_url ? resolveAssetUrl(upload.original_url) : undefined);
  const [selectedStyle, setSelectedStyle] = useState<StyleType>("signature_minimal");

  const categoryOptions: Array<{ id: JewelleryType; label: string; Icon: typeof Gem; description: string }> = [
    { id: "earrings", label: "Earrings", Icon: Gem, description: "Studs, drops, hoops, and luxury jhumka-inspired looks." },
    { id: "necklace", label: "Necklace", Icon: ShieldCheck, description: "Pendant, solitaire drop, collar, and bridal necklines." },
    { id: "ring", label: "Ring", Icon: Circle, description: "Solitaire, halo, and couture gemstone ring looks." },
    { id: "nose_pin", label: "Nose Pin", Icon: ScanFace, description: "Solitaire and halo nose pin previews with refined scale." },
  ];

  const styleOptions: Array<{ id: StyleType; label: string; copy: string }> = [
    { id: "signature_minimal", label: "Signature Minimal", copy: "Delicate, clean, understated luxury." },
    { id: "evening_elegance", label: "Evening Elegance", copy: "Radiant pieces with polished evening presence." },
    { id: "bridal_heirloom", label: "Bridal Heirloom", copy: "Ornate craftsmanship with heirloom depth." },
    { id: "contemporary_couture", label: "Contemporary Couture", copy: "Modern lines and high-fashion confidence." },
  ];

  const categoryDefaults: Record<
    JewelleryType,
    { style: StyleType; scale: ScaleType; variant: string }
  > = {
    earrings: { style: "signature_minimal", scale: "refined", variant: "studs" },
    necklace: { style: "evening_elegance", scale: "statement", variant: "pendant" },
    nose_pin: { style: "signature_minimal", scale: "refined", variant: "solitaire" },
    ring: { style: "contemporary_couture", scale: "statement", variant: "solitaire_ring" },
  };

  const uploadMutation = useMutation({
    mutationFn: async (file: File) => {
      setPreviewUrl(URL.createObjectURL(file));
      const uploadResponse = await uploadPortrait(file);
      const analysisResponse = await analyzePortrait(uploadResponse.image_id);
      return { uploadResponse, analysisResponse };
    },
    onSuccess: ({ uploadResponse, analysisResponse }) => {
      setUpload(uploadResponse);
      setAnalysis(analysisResponse);
      setPreviewUrl(resolveAssetUrl(uploadResponse.original_url));
      if (analysisResponse.detectedInfo.faces !== 1) {
        navigate("/unsupported");
      }
    },
  });

  const generateMutation = useMutation({
    mutationFn: (payload: GenerateRequest) => generatePreview(payload),
    onSuccess: (response) => {
      setResults(response);
      navigate("/results");
    },
  });

  const loadingStep = useMemo(() => {
    if (uploadMutation.isPending) return 0;
    if (generateMutation.isPending) return 1;
    return 2;
  }, [uploadMutation.isPending, generateMutation.isPending]);

  const generateLooks = () => {
    if (!upload?.image_id) return;
    const category = selectedCategory || "earrings";
    if (!upload?.image_id) return;
    const defaults = categoryDefaults[category];
    generateMutation.mutate({
      image_id: upload.image_id,
      jewelleryType: category,
      metal: selectedMetal,
      stone: selectedStone,
      style: selectedStyle || defaults.style,
      scale: defaults.scale,
      variant: defaults.variant,
      placement: {
        side: "left",
        finger: "ring",
      },
      variants: 3,
    });
  };

  return (
    <div className="min-h-screen bg-zinc-950 font-sans text-zinc-50 antialiased selection:bg-amber-200/30">
      <nav className="sticky top-0 z-50 flex w-full items-center justify-between border-b border-zinc-900/80 bg-zinc-950/90 px-5 py-4 backdrop-blur">
        <Link to="/" className="text-xs uppercase tracking-[0.2em] text-zinc-500 transition-colors hover:text-zinc-300">
          Home
        </Link>
        <h1 className="font-serif text-xl uppercase tracking-[0.3em] text-zinc-100">Aurelium</h1>
        <div className="w-10" />
      </nav>
      <main className="mx-auto flex w-full max-w-7xl flex-col gap-8 px-4 py-6 md:px-6 md:py-10">
        <section className="rounded-[2rem] border border-zinc-800 bg-[radial-gradient(circle_at_top,rgba(217,177,103,0.12),transparent_30%),linear-gradient(180deg,#17171a_0%,#0d0d10_100%)] p-6 md:p-10">
          <div className="max-w-3xl">
            <p className="text-xs uppercase tracking-[0.24em] text-amber-200/80">Private Jewellery Preview</p>
            <h1 className="mt-4 font-serif text-4xl leading-tight text-zinc-100 md:text-6xl">
              Upload your portrait, choose a style, and preview refined luxury looks.
            </h1>
            <p className="mt-4 max-w-2xl text-sm leading-7 text-zinc-400 md:text-base">
              Aurelium keeps the process simple. Begin with one portrait, select the jewellery category you want to explore, choose a style direction, and generate your curated try-on results in the final section below.
            </p>
          </div>
        </section>

        <section className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr]">
          <div className="rounded-[2rem] border border-zinc-800 bg-zinc-900/60 p-5 md:p-6">
            <div className="mb-5">
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Step 1</p>
              <h2 className="mt-2 font-serif text-2xl text-zinc-100 md:text-3xl">Upload your portrait</h2>
              <p className="mt-2 text-sm leading-7 text-zinc-400">
                Use one portrait with a clear face. Visible neckline helps necklace previews. Visible hand helps ring previews.
              </p>
            </div>

            <button
              onClick={() => document.getElementById("portrait-upload")?.click()}
              className="group relative flex min-h-[360px] w-full flex-col items-center justify-center gap-4 overflow-hidden rounded-[1.6rem] border border-dashed border-zinc-700 bg-zinc-950/40 transition-all duration-500 hover:border-amber-200/50 hover:bg-zinc-900/80"
            >
              <input
                id="portrait-upload"
                type="file"
                accept="image/*"
                className="hidden"
                onChange={(event) => {
                  const file = event.target.files?.[0];
                  if (file) uploadMutation.mutate(file);
                }}
              />
              {previewUrl ? (
                <img src={previewUrl} alt="Portrait preview" className="h-full max-h-[560px] w-full rounded-[1.4rem] object-cover" />
              ) : (
                <>
                  <div className="flex h-16 w-16 items-center justify-center rounded-full bg-zinc-900 transition-transform duration-500 group-hover:scale-110">
                    <Camera className="text-zinc-400 group-hover:text-amber-200/80" size={24} />
                  </div>
                  <span className="text-sm uppercase tracking-widest text-zinc-400">Tap to Capture / Upload</span>
                </>
              )}
            </button>

            {analysis?.qualityWarnings?.length ? (
              <div className="mt-4 rounded-2xl border border-zinc-800 bg-zinc-950/50 p-4 text-sm text-zinc-400">
                {analysis.qualityWarnings[0]}
              </div>
            ) : null}

            {uploadMutation.error ? <p className="mt-4 text-sm text-red-400">{String(uploadMutation.error)}</p> : null}
          </div>

          <div className="space-y-8">
            <section className="rounded-[2rem] border border-zinc-800 bg-zinc-900/60 p-5 md:p-6">
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Step 2</p>
              <h2 className="mt-2 font-serif text-2xl text-zinc-100 md:text-3xl">Choose your focus</h2>
              <p className="mt-2 text-sm leading-7 text-zinc-400">Select the jewellery category you want Aurelium to preview on your portrait.</p>
              <div className="mt-6 grid gap-4 sm:grid-cols-2">
                {categoryOptions.map((cat) => {
                  const active = selectedCategory === cat.id;
                  return (
                    <button
                      key={cat.id}
                      type="button"
                      onClick={() => setSelectedCategory(cat.id)}
                      className={`rounded-[1.4rem] border p-5 text-left transition-all duration-300 ${
                        active ? "border-amber-200/60 bg-amber-200/8" : "border-zinc-800 bg-zinc-950/40 hover:border-zinc-700"
                      }`}
                    >
                      <cat.Icon className="mb-4 h-6 w-6 text-amber-200/80" strokeWidth={1.5} />
                      <p className="font-serif text-xl text-zinc-100">{cat.label}</p>
                      <p className="mt-2 text-sm leading-6 text-zinc-400">{cat.description}</p>
                    </button>
                  );
                })}
              </div>
            </section>

            <section className="rounded-[2rem] border border-zinc-800 bg-zinc-900/60 p-5 md:p-6">
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Step 3</p>
              <h2 className="mt-2 font-serif text-2xl text-zinc-100 md:text-3xl">Choose your style</h2>
              <p className="mt-2 text-sm leading-7 text-zinc-400">Pick the style direction you want the generated looks to follow.</p>
              <div className="mt-6 grid gap-4 md:grid-cols-2">
                {styleOptions.map((style) => {
                  const active = selectedStyle === style.id;
                  return (
                    <button
                      key={style.id}
                      type="button"
                      onClick={() => setSelectedStyle(style.id)}
                      className={`rounded-[1.4rem] border p-5 text-left transition-all duration-300 ${
                        active ? "border-amber-200/60 bg-amber-200/8" : "border-zinc-800 bg-zinc-950/40 hover:border-zinc-700"
                      }`}
                    >
                      <p className="font-serif text-xl text-zinc-100">{style.label}</p>
                      <p className="mt-2 text-sm leading-6 text-zinc-400">{style.copy}</p>
                    </button>
                  );
                })}
              </div>
            </section>

            <section className="rounded-[2rem] border border-zinc-800 bg-zinc-900/60 p-5 md:p-6">
              <p className="text-xs uppercase tracking-[0.22em] text-zinc-500">Step 4</p>
              <h2 className="mt-2 font-serif text-2xl text-zinc-100 md:text-3xl">Generate your looks</h2>
              <p className="mt-2 text-sm leading-7 text-zinc-400">
                Aurelium will create a small curated set of premium previews based on your portrait, chosen category, and style direction.
              </p>
              <button
                onClick={generateLooks}
                disabled={!upload?.image_id || generateMutation.isPending}
                className="mt-6 inline-flex w-full items-center justify-center gap-3 rounded-full bg-zinc-100 px-6 py-4 text-sm font-medium uppercase tracking-widest text-zinc-900 transition-all duration-300 hover:bg-white disabled:cursor-not-allowed disabled:opacity-60"
              >
                {generateMutation.isPending ? <Sparkles size={16} className="animate-pulse" /> : <ChevronRight size={16} />}
                {generateMutation.isPending ? "Generating Looks" : "Generate Output"}
              </button>
              {generateMutation.error ? <p className="mt-4 text-sm text-red-400">{String(generateMutation.error)}</p> : null}
            </section>
          </div>
        </section>
      </main>
    </div>
  );
}

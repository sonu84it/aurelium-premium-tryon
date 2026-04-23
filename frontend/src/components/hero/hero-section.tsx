export function HeroSection() {
  return (
    <section className="relative overflow-hidden bg-zinc-950">
      <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,rgba(217,177,103,0.2),transparent_28%),radial-gradient(circle_at_80%_18%,rgba(255,255,255,0.07),transparent_22%),linear-gradient(180deg,#0f0f10_0%,#09090b_100%)]" />
      <div className="absolute left-[8%] top-[10%] h-40 w-40 rounded-full border border-amber-200/10 bg-amber-200/5 blur-3xl" />
      <div className="absolute bottom-[12%] right-[10%] h-44 w-44 rounded-full border border-zinc-100/10 bg-zinc-100/5 blur-3xl" />
      <div className="relative z-10 mx-auto grid w-full max-w-7xl gap-8 px-4 py-16 md:px-6 md:py-24 xl:grid-cols-[1.05fr_0.95fr] xl:items-center">
        <div className="max-w-3xl">
          <p className="text-xs uppercase tracking-[0.32em] text-amber-200/80">Private Jewellery Consultation</p>
          <h1 className="mt-6 font-serif text-5xl leading-[0.95] text-zinc-100 sm:text-6xl md:text-7xl xl:text-[6.2rem]">
            Discover your
            <span className="mt-2 block italic text-amber-200/85">signature piece.</span>
          </h1>
          <p className="mt-6 max-w-2xl text-base leading-8 text-zinc-400 md:text-lg">
            Upload your portrait, select the jewellery focus you want to explore, and let Aurelium compose refined premium looks with a guided luxury experience.
          </p>
          <div className="mt-10 flex flex-wrap gap-3 text-[11px] uppercase tracking-[0.22em] text-zinc-500">
            <span className="rounded-full border border-zinc-800 bg-zinc-900/60 px-4 py-2">One Portrait</span>
            <span className="rounded-full border border-zinc-800 bg-zinc-900/60 px-4 py-2">One Focus</span>
            <span className="rounded-full border border-zinc-800 bg-zinc-900/60 px-4 py-2">Curated Results</span>
          </div>
        </div>
        <div className="grid gap-4 md:grid-cols-[1.05fr_0.95fr]">
          <div className="relative overflow-hidden rounded-[2rem] border border-zinc-800/80 bg-[radial-gradient(circle_at_top,#5f4a34_0%,#241b14_48%,#0b0b0c_100%)] p-4">
            <div className="relative aspect-[4/5] overflow-hidden rounded-[1.5rem] border border-white/8 bg-zinc-950">
              <img
                src="/static/HomePage.png"
                alt="Aurelium luxury portrait"
                className="h-full w-full object-cover object-center"
              />
              <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(9,9,11,0.06),rgba(9,9,11,0.28))]" />
              <div className="absolute left-[8%] top-[10%] h-16 w-16 rounded-full bg-amber-100/8 blur-2xl" />
              <div className="absolute bottom-[8%] right-[8%] h-24 w-24 rounded-full bg-amber-200/10 blur-3xl" />
            </div>
          </div>
          <div className="flex flex-col justify-between rounded-[2rem] border border-zinc-800 bg-zinc-900/80 p-6 text-left text-zinc-100">
            <div>
              <p className="text-sm uppercase tracking-[0.24em] text-amber-200/80">Signature Edit</p>
              <p className="mt-6 font-serif text-4xl leading-tight md:text-[2.9rem]">Diamond Solstice Studs</p>
              <p className="mt-5 text-base leading-8 text-zinc-400">
                Identity preserved. Placement refined. Crafted for exceptional gold, platinum, and precious stone finishes.
              </p>
            </div>
            <div className="mt-10 grid grid-cols-3 gap-3 text-[11px] uppercase tracking-[0.2em] text-zinc-500">
              <span>Diamond</span>
              <span>Yellow Gold</span>
              <span>Refined Finish</span>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

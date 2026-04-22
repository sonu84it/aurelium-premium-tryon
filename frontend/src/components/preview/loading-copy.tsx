const messages = [
  "Analyzing placement and proportions",
  "Composing a refined jewellery preview",
  "Rendering premium finish and detail",
];

export function LoadingCopy({ step }: { step: number }) {
  return <p className="text-sm tracking-[0.18em] text-charcoal/65 uppercase">{messages[step % messages.length]}</p>;
}

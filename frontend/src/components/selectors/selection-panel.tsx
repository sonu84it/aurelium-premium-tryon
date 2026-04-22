import type { JewelleryType, MetalType, ScaleType, StoneType, StyleType } from "@/types";

import { Card } from "@/components/common/card";
import { cn } from "@/lib/utils";

const categoryOptions: Array<{ label: string; value: JewelleryType }> = [
  { label: "Earrings", value: "earrings" },
  { label: "Necklace", value: "necklace" },
  { label: "Nose Pin", value: "nose_pin" },
  { label: "Ring", value: "ring" },
];

const metalOptions: Array<{ label: string; value: MetalType }> = [
  { label: "Yellow Gold", value: "yellow_gold" },
  { label: "White Gold", value: "white_gold" },
  { label: "Rose Gold", value: "rose_gold" },
  { label: "Platinum", value: "platinum" },
];

const stoneOptions: Array<{ label: string; value: StoneType }> = [
  { label: "Diamond", value: "diamond" },
  { label: "Emerald", value: "emerald" },
  { label: "Ruby", value: "ruby" },
  { label: "Sapphire", value: "sapphire" },
];

const styleOptions: Array<{ label: string; value: StyleType }> = [
  { label: "Signature Minimal", value: "signature_minimal" },
  { label: "Evening Elegance", value: "evening_elegance" },
  { label: "Bridal Heirloom", value: "bridal_heirloom" },
  { label: "Contemporary Couture", value: "contemporary_couture" },
];

const scaleOptions: Array<{ label: string; value: ScaleType }> = [
  { label: "Refined", value: "refined" },
  { label: "Statement", value: "statement" },
  { label: "Grand", value: "grand" },
];

const variantMap: Record<JewelleryType, string[]> = {
  earrings: ["studs", "hoops", "drop", "jhumka_luxury"],
  necklace: ["pendant", "solitaire_drop", "collar", "bridal_set"],
  nose_pin: ["solitaire", "halo", "floral_diamond"],
  ring: ["solitaire_ring", "halo_ring", "emerald_cut", "ruby_statement", "sapphire_signature"],
};

interface Props {
  availableZones?: Record<string, { available: boolean; reason?: string }>;
  category: JewelleryType;
  metal: MetalType;
  stone: StoneType;
  style: StyleType;
  scale: ScaleType;
  variant: string;
  onChange: (next: Partial<Props>) => void;
}

function OptionGrid<T extends string>({
  label,
  options,
  value,
  onChange,
  disabledValues,
}: {
  label: string;
  options: Array<{ label: string; value: T }>;
  value: T;
  onChange: (value: T) => void;
  disabledValues?: string[];
}) {
  return (
    <div>
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.22em] text-charcoal/55">{label}</p>
      <div className="grid grid-cols-2 gap-3">
        {options.map((option) => {
          const disabled = disabledValues?.includes(option.value);
          return (
            <button
              key={option.value}
              type="button"
              disabled={disabled}
              onClick={() => onChange(option.value)}
              className={cn(
                "rounded-[1.2rem] border px-4 py-3 text-left text-sm transition",
                value === option.value ? "border-gold bg-gold/10 text-charcoal" : "border-charcoal/10 bg-white/80 text-charcoal/78",
                disabled && "cursor-not-allowed opacity-40",
              )}
            >
              {option.label}
            </button>
          );
        })}
      </div>
    </div>
  );
}

export function SelectionPanel(props: Props) {
  const unavailable = Object.entries(props.availableZones ?? {})
    .filter(([, value]) => !value.available)
    .map(([key]) => (key === "nosePin" ? "nose_pin" : key));

  return (
    <Card className="space-y-6">
      <OptionGrid label="Category" options={categoryOptions} value={props.category} onChange={(category) => props.onChange({ category })} disabledValues={unavailable} />
      <OptionGrid label="Metal" options={metalOptions} value={props.metal} onChange={(metal) => props.onChange({ metal })} />
      <OptionGrid label="Gemstone" options={stoneOptions} value={props.stone} onChange={(stone) => props.onChange({ stone })} />
      <OptionGrid label="Style" options={styleOptions} value={props.style} onChange={(style) => props.onChange({ style })} />
      <OptionGrid label="Scale" options={scaleOptions} value={props.scale} onChange={(scale) => props.onChange({ scale })} />
      <OptionGrid
        label="Design preset"
        options={variantMap[props.category].map((value) => ({ label: value.replace(/_/g, " "), value }))}
        value={props.variant}
        onChange={(variant) => props.onChange({ variant })}
      />
    </Card>
  );
}

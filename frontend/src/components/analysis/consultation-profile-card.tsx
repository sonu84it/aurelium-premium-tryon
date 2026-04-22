import type { AgeBandType, ConsultationProfile, PresentationType } from "@/types";

import { Card } from "@/components/common/card";
import { cn } from "@/lib/utils";

const presentationOptions: Array<{ label: string; value: PresentationType }> = [
  { label: "Feminine", value: "feminine" },
  { label: "Masculine", value: "masculine" },
  { label: "Universal", value: "universal" },
];

const ageBandOptions: Array<{ label: string; value: AgeBandType }> = [
  { label: "Under 30", value: "under_30" },
  { label: "30 to 50", value: "between_30_and_50" },
  { label: "Over 50", value: "over_50" },
];

function OptionRow<T extends string>({
  label,
  options,
  value,
  onChange,
}: {
  label: string;
  options: Array<{ label: string; value: T }>;
  value?: T;
  onChange: (value: T) => void;
}) {
  return (
    <div>
      <p className="mb-3 text-xs font-semibold uppercase tracking-[0.22em] text-charcoal/55">{label}</p>
      <div className="grid grid-cols-3 gap-3">
        {options.map((option) => (
          <button
            key={option.value}
            type="button"
            onClick={() => onChange(option.value)}
            className={cn(
              "rounded-[1.2rem] border px-4 py-3 text-sm transition",
              value === option.value ? "border-gold bg-gold/10 text-charcoal" : "border-charcoal/10 bg-white/80 text-charcoal/78",
            )}
          >
            {option.label}
          </button>
        ))}
      </div>
    </div>
  );
}

export function ConsultationProfileCard({
  profile,
  onChange,
}: {
  profile: ConsultationProfile;
  onChange: (profile: ConsultationProfile) => void;
}) {
  return (
    <Card>
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-charcoal/55">Consultation profile</p>
      <h2 className="mt-3 font-display text-4xl text-charcoal">Tailor suggestions to your preference</h2>
      <p className="mt-3 text-sm leading-7 text-charcoal/72">
        This is optional and user-selected. Aurelium does not infer gender or age from portraits automatically.
      </p>
      <div className="mt-6 space-y-6">
        <OptionRow
          label="Presentation"
          options={presentationOptions}
          value={profile.presentation}
          onChange={(presentation) => onChange({ ...profile, presentation })}
        />
        <OptionRow
          label="Age band"
          options={ageBandOptions}
          value={profile.ageBand}
          onChange={(ageBand) => onChange({ ...profile, ageBand })}
        />
      </div>
    </Card>
  );
}

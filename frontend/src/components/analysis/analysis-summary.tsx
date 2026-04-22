import { Card } from "@/components/common/card";
import type { AnalyzeResponse } from "@/types";

export function AnalysisSummary({ analysis }: { analysis: AnalyzeResponse }) {
  return (
    <Card>
      <p className="text-xs font-semibold uppercase tracking-[0.22em] text-charcoal/55">Consultation insight</p>
      <h2 className="mt-3 font-display text-4xl text-charcoal">Portrait suitability</h2>
      {analysis.consultationProfile ? (
        <p className="mt-3 text-sm leading-6 text-charcoal/62">
          Suggestions were tailored using your selected consultation profile.
        </p>
      ) : null}
      <div className="mt-6 space-y-3">
        {analysis.luxuryRecommendations.map((recommendation) => (
          <p key={recommendation} className="text-sm leading-6 text-charcoal/78">
            {recommendation}
          </p>
        ))}
        {analysis.qualityWarnings.map((warning) => (
          <p key={warning} className="text-sm leading-6 text-stone">
            {warning}
          </p>
        ))}
      </div>
    </Card>
  );
}

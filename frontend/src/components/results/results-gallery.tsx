import { ReactCompareSlider, ReactCompareSliderImage } from "react-compare-slider";

import { resolveAssetUrl } from "@/services/api";
import { Card } from "@/components/common/card";
import type { GenerateResponse } from "@/types";

export function ResultsGallery({ originalUrl, results }: { originalUrl: string; results: GenerateResponse }) {
  const featured = results.results[0];
  return (
    <div className="grid gap-6 lg:grid-cols-[1.3fr_0.7fr]">
      <Card className="overflow-hidden p-3">
        <ReactCompareSlider
          itemOne={<ReactCompareSliderImage src={resolveAssetUrl(originalUrl)} alt="Original portrait" />}
          itemTwo={<ReactCompareSliderImage src={resolveAssetUrl(featured.url)} alt={featured.title} />}
        />
      </Card>
      <div className="space-y-4">
        {results.results.map((result) => (
          <Card key={result.url}>
            <img src={resolveAssetUrl(result.url)} alt={result.title} className="aspect-[4/5] w-full rounded-[1.4rem] object-cover" />
            <p className="mt-4 font-display text-3xl text-charcoal">{result.title}</p>
            <a href={resolveAssetUrl(result.url)} download className="mt-3 inline-block text-sm text-charcoal/72 underline underline-offset-4">
              Download high-resolution image
            </a>
          </Card>
        ))}
      </div>
    </div>
  );
}

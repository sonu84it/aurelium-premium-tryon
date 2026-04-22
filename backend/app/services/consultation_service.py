from __future__ import annotations

from typing import List

from app.models.schemas import AgeBandType, ConsultationProfile, PresentationType


class ConsultationService:
    def build_recommendations(self, profile: ConsultationProfile | None) -> List[str]:
        if profile is None:
            return []

        recommendations: List[str] = []

        if profile.presentation == PresentationType.feminine:
            recommendations.append("Refined drop earrings, halo pendants, and solitaire nose pins tend to suit this consultation profile beautifully.")
        elif profile.presentation == PresentationType.masculine:
            recommendations.append("Cleaner pendant lines, signet-inspired rings, and restrained diamond accents suit this consultation profile well.")
        elif profile.presentation == PresentationType.universal:
            recommendations.append("Minimal studs, elegant pendants, and tailored gemstone rings offer the most versatile luxury direction here.")

        if profile.ageBand == AgeBandType.under_30:
            recommendations.append("Contemporary couture and signature minimal settings are the strongest starting point for this age band.")
        elif profile.ageBand == AgeBandType.between_30_and_50:
            recommendations.append("Evening elegance and balanced statement scale usually create the most polished result for this age band.")
        elif profile.ageBand == AgeBandType.over_50:
            recommendations.append("Bridal heirloom detailing, refined platinum, and emerald or sapphire accents often feel especially elevated for this age band.")

        return recommendations

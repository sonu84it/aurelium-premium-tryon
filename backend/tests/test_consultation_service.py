from app.models.schemas import AgeBandType, ConsultationProfile, PresentationType
from app.services.consultation_service import ConsultationService


def test_consultation_recommendations_respect_profile() -> None:
    profile = ConsultationProfile(
        presentation=PresentationType.feminine,
        ageBand=AgeBandType.between_30_and_50,
    )
    recommendations = ConsultationService().build_recommendations(profile)
    assert len(recommendations) == 2
    assert "drop earrings" in recommendations[0]
    assert "age band" in recommendations[1]

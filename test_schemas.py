from src.schemas import PhotographerCapabilities, ArtistIntelligence, Confidence, Evidence
import json

try:
    p = PhotographerCapabilities(subjects=["product"], settings=["studio"])
    print("PhotographerCapabilities OK")

    e = Evidence(
        source_file="test.jpg",
        media_id="img1",
        source_type="image",
        observation="Test observation",
        supports=["product"],
        strength="medium"
    )
    print("Evidence OK")

    c = Confidence(level="high", reason="Clear evidence")
    print("Confidence OK")
    
    ai = ArtistIntelligence(
        artist_id="P01",
        category="photographer",
        profile_claims=["product"],
        demonstrated_capabilities=p,
        evidence=[e],
        unknowns=[],
        confidence=c
    )
    print("ArtistIntelligence OK")
    print(ai.model_dump_json(indent=2))

except Exception as ex:
    print("Validation failed:", ex)


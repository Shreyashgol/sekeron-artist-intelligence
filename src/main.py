import os
import logging
from src.ingestion import scan_data_directory
from src.capability_extractor import process_all_artists
from src.recommendation_generator import RecommendationGenerator
from src.re_ranker import ReRanker
from src.schemas import ArtistIntelligence
import glob
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_artist_intelligence():
    logger.info("Starting dataset scan...")
    records = scan_data_directory()
    
    if not records:
        logger.error("No artists found! Check data directory.")
        return
        
    out_path = "outputs/artist_intelligence.jsonl"
    logger.info(f"Extracting capabilities and writing to {out_path}...")
    process_all_artists(records, out_path)
    logger.info("Done generating artist intelligence.")
    
    # Load intel back
    artists = []
    with open(out_path, 'r') as f:
        for line in f:
            if line.strip():
                artists.append(ArtistIntelligence.model_validate_json(line))
                
    logger.info("Generating recommendations...")
    briefs = glob.glob("data/hirer_conversations/*.txt")
    generator = RecommendationGenerator()
    
    if not briefs:
        logger.warning("No hirer conversation files found in data/hirer_conversations/. Skipping recommendations.")
        with open("outputs/recommendations.json", "w") as f:
            json.dump([], f, indent=2)
        return
    
    recommendations = generator.generate(briefs, artists)
    
    with open("outputs/recommendations.json", "w") as f:
        json.dump([r.model_dump() for r in recommendations], f, indent=2)
    logger.info(f"Done generating {len(recommendations)} recommendations.")
    
    # --- Follow-up re-ranking ---
    logger.info("Handling follow-up re-ranking...")
    cafe_brief_path = "data/hirer_conversations/01_cafe_music_whatsapp.txt"
    
    if not os.path.exists(cafe_brief_path):
        logger.warning(f"Follow-up brief {cafe_brief_path} not found. Skipping re-ranking.")
        return
    
    re_ranker = ReRanker()
    cafe_intent = generator.parser.parse_intent(cafe_brief_path)
    
    # Find the cafe music recommendation (brief_id is the filename stem)
    cafe_recommendation = next(
        (r for r in recommendations if r.brief_id == "01_cafe_music_whatsapp"), None
    )
    
    if not cafe_recommendation or not cafe_recommendation.top_candidates:
        logger.warning("No café music recommendation found or no candidates ranked. Skipping re-ranking.")
        return
    
    original_candidates = cafe_recommendation.top_candidates
    follow_up_res = re_ranker.re_rank(cafe_intent, artists, original_candidates)
    
    with open("outputs/updated_recommendation.json", "w") as f:
        json.dump(follow_up_res.model_dump(), f, indent=2)
    logger.info("Done generating follow-up recommendations.")

if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    generate_artist_intelligence()

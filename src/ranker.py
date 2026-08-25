from typing import List, Dict, Any
from src.schemas import HirerIntent, ArtistIntelligence, CandidateRecommendation, ImprovementQuestion, Unknown

class Ranker:
    def rank(self, intent: HirerIntent, artists: List[ArtistIntelligence]) -> List[CandidateRecommendation]:
        candidates = []
        
        # Only consider artists in the same category
        relevant_artists = [a for a in artists if a.category == intent.category]
        
        for artist in relevant_artists:
            base_score = 50.0
            factor_scores = {}
            matched = []
            unmatched = []
            trade_offs = []
            
            # Simple heuristic matching
            # In a full system, this would do semantic comparison between intent requirements and capabilities
            
            if "acoustic" in " ".join(intent.explicit_requirements).lower():
                if isinstance(artist.demonstrated_capabilities, dict):
                    genres = artist.demonstrated_capabilities.get('genres', [])
                else:
                    genres = getattr(artist.demonstrated_capabilities, 'genres', [])
                    
                if "acoustic" in genres:
                    matched.append("Acoustic format")
                    base_score += 20
                else:
                    unmatched.append("Acoustic format")
                    base_score -= 10
                    trade_offs.append("Not primarily an acoustic artist")
                    
            if "product" in " ".join(intent.explicit_requirements).lower():
                if hasattr(artist.demonstrated_capabilities, 'subjects'):
                    subjects = artist.demonstrated_capabilities.subjects
                    if "product" in subjects:
                        matched.append("Product photography")
                        base_score += 20
                    else:
                        unmatched.append("Product photography")
                        base_score -= 10
                        trade_offs.append("Doesn't specialize in product photography")
                        
            # Confidence multiplier
            conf_map = {"high": 1.0, "medium": 0.8, "low": 0.5, "reduced": 0.3}
            multiplier = conf_map.get(artist.confidence.level, 0.5)
            
            final_score = base_score * multiplier
            factor_scores["base_match"] = base_score
            factor_scores["confidence_multiplier"] = multiplier
            
            # Mock assumptions
            assumptions = ["Assuming they are available on the requested date"]
            
            candidates.append(CandidateRecommendation(
                artist_id=artist.artist_id,
                total_score=final_score,
                factor_scores=factor_scores,
                matched_requirements=matched,
                unmatched_requirements=unmatched,
                supporting_evidence=artist.evidence,
                trade_offs=trade_offs,
                unknowns=artist.unknowns,
                confidence=artist.confidence,
                assumptions=assumptions
            ))
            
        # Sort candidates descending by score
        candidates.sort(key=lambda x: x.total_score, reverse=True)
        return candidates


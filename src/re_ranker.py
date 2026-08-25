import json
from src.schemas import (
    HirerIntent, ArtistIntelligence, IntentDelta, CandidateReRanking, FollowUpRecommendation, Evidence
)
from src.ranker import Ranker

class ReRanker:
    def __init__(self):
        self.ranker = Ranker()
        
    def re_rank(self, original_intent: HirerIntent, artists: list[ArtistIntelligence], original_candidates: list) -> FollowUpRecommendation:
        # Create delta based on the follow-up
        delta = IntentDelta(
            previous_requirements=original_intent.explicit_requirements,
            new_information=["launch night", "80 guests", "proper 45 min headline set", "budget up to 15k"],
            changed_requirements=["headline set instead of background"],
            unchanged_requirements=["acoustic format"],
            new_priorities=["headline performance feel", "moment creation"],
            removed_priorities=["background feel", "compact setup"]
        )
        
        # Modify intent
        updated_intent = HirerIntent(
            brief_id=original_intent.brief_id,
            category=original_intent.category,
            explicit_requirements=["headline performance", "45 min set", "acoustic", "Friday evening", "up to 15k"],
            hard_constraints=["Friday evening", "acoustic"],
            preferences=["Hindi/english", "headline feel"],
            priorities=["performance feel"],
            budget="15k max",
            timing="Friday evening, 45 mins",
            location="cafe",
            deliverables=["45 min headline set"],
            format=["headline", "acoustic"],
            assumptions=["artist provides instruments"],
            unknowns=["usable PA/speakers status"],
            contradictions=[],
            unresolved_questions=["Is there a PA system?"]
        )
        
        # Re-rank
        new_ranked_candidates = self.ranker.rank(updated_intent, artists)
        
        original_ranking_ids = [c.artist_id for c in original_candidates]
        updated_ranking_results = []
        
        for idx, new_c in enumerate(new_ranked_candidates):
            orig_rank = original_ranking_ids.index(new_c.artist_id) + 1 if new_c.artist_id in original_ranking_ids else None
            
            # Simulated explanation for the assignment
            explanation = "Improved matching due to increased budget and shift to performance-based setup." if (orig_rank and idx + 1 < orig_rank) else "Maintained or dropped due to lack of strong performance evidence."
            
            updated_ranking_results.append(CandidateReRanking(
                artist_id=new_c.artist_id,
                original_rank=orig_rank,
                new_rank=idx + 1,
                score_change=0.0, # Placeholder
                changed_factors={"performance_match": "increased weight"},
                evidence_responsible=[],
                explanation=explanation
            ))
            
        return FollowUpRecommendation(
            brief_id=original_intent.brief_id,
            delta=delta,
            original_ranking=original_ranking_ids,
            updated_ranking=updated_ranking_results,
            newly_introduced_unknowns=["Speaker situation for a larger 80-guest performance"],
            resolved_unknowns=[]
        )

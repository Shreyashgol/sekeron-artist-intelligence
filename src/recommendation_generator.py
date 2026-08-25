import json
import logging
from typing import List
from pathlib import Path
from pydantic import BaseModel
from src.schemas import HirerIntent, ArtistIntelligence, BriefRecommendation, ImprovementQuestion
from src.ranker import Ranker
from src.intent_parser import IntentParser
from src.llm_client import LLMClient

logger = logging.getLogger(__name__)

class ExplanationResult(BaseModel):
    why_match: List[str]
    supporting_evidence: List[str]
    trade_offs: List[str]
    unknowns: List[str]
    confidence: str
    improvement_questions: List[ImprovementQuestion]

class RecommendationGenerator:
    def __init__(self):
        self.ranker = Ranker()
        self.parser = IntentParser()
        self.llm_client = LLMClient()
        
        prompt_path = Path("prompts /model_prompts/recommendation explanation prompt.md")
        if prompt_path.exists():
            self.system_prompt = prompt_path.read_text()
        else:
            logger.warning(f"Prompt template not found at {prompt_path}, using default.")
            self.system_prompt = "You are NOT the ranking engine. Explain the already-computed result."

    def generate(self, briefs_paths: List[str], artists: List[ArtistIntelligence]) -> List[BriefRecommendation]:
        recommendations = []
        for path in briefs_paths:
            intent = self.parser.parse_intent(path)
            if intent.category == "unknown":
                continue
                
            ranked_candidates = self.ranker.rank(intent, artists)
            top_2 = ranked_candidates[:2]
            
            all_questions = []
            
            for candidate in top_2:
                # Use LLM to generate the explanation and improvement questions
                artist = next((a for a in artists if a.artist_id == candidate.artist_id), None)
                if not artist:
                    continue
                    
                user_prompt = (
                    f"Hirer Requirements: {json.dumps(intent.explicit_requirements + intent.hard_constraints)}\n"
                    f"Artist Capabilities: {artist.demonstrated_capabilities}\n"
                    f"Score Breakdown: {json.dumps(candidate.factor_scores)}\n"
                    f"Trade-offs: {json.dumps(candidate.trade_offs)}\n"
                    f"Unknowns: {json.dumps([u.model_dump() for u in candidate.unknowns])}\n"
                )
                
                try:
                    explanation = self.llm_client.generate_structured(self.system_prompt, user_prompt, ExplanationResult)
                    candidate.trade_offs.extend(explanation.trade_offs)
                    all_questions.extend(explanation.improvement_questions)
                except Exception as e:
                    logger.error(f"Failed to generate explanation for {candidate.artist_id}: {e}")
                    
            # Deduplicate questions by question text
            unique_questions = []
            seen = set()
            for q in all_questions:
                if q.question not in seen:
                    unique_questions.append(q)
                    seen.add(q.question)
                    
            recommendations.append(BriefRecommendation(
                brief_id=intent.brief_id,
                top_candidates=top_2,
                improvement_questions=unique_questions[:2] # Max 2 questions as per rule
            ))
            
        return recommendations

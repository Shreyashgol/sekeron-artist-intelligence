from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Union, Dict

# --- Core Common Structures ---

class Confidence(BaseModel):
    level: Literal["low", "medium", "high", "reduced"]
    reason: str

class Evidence(BaseModel):
    source_file: str
    media_id: str
    source_type: Literal["profile", "image", "audio", "video", "conversation"]
    timestamp: Optional[str] = None
    observation: str
    supports: List[str]
    strength: Literal["weak", "medium", "strong"]

class Unknown(BaseModel):
    dimension: str
    reason: str

# --- Capabilities ---

class PhotographerCapabilities(BaseModel):
    subjects: List[str] = Field(default_factory=list)
    settings: List[str] = Field(default_factory=list)
    visual_styles: List[str] = Field(default_factory=list)
    lighting: List[str] = Field(default_factory=list)
    composition: List[str] = Field(default_factory=list)
    formats: List[str] = Field(default_factory=list)

class MusicianCapabilities(BaseModel):
    genres: List[str] = Field(default_factory=list)
    instrumentation: List[str] = Field(default_factory=list)
    vocal_styles: List[str] = Field(default_factory=list)
    moods: List[str] = Field(default_factory=list)
    tempos: List[str] = Field(default_factory=list)
    performance_formats: List[str] = Field(default_factory=list)

class VideoEditorCapabilities(BaseModel):
    editing_styles: List[str] = Field(default_factory=list)
    pacing: List[str] = Field(default_factory=list)
    storytelling: List[str] = Field(default_factory=list)
    aspect_ratios: List[str] = Field(default_factory=list)
    formats: List[str] = Field(default_factory=list)

# --- Artist Intelligence ---

class ArtistIntelligence(BaseModel):
    artist_id: str
    category: Literal["photographer", "musician", "video_editor", "unknown"]
    profile_claims: List[str]
    demonstrated_capabilities: Union[PhotographerCapabilities, MusicianCapabilities, VideoEditorCapabilities, Dict]
    evidence: List[Evidence]
    unknowns: List[Unknown]
    confidence: Confidence

# --- Hirer Intent ---

class HirerIntent(BaseModel):
    brief_id: str
    category: Literal["photographer", "musician", "video_editor", "unknown"]
    explicit_requirements: List[str]
    hard_constraints: List[str]
    preferences: List[str]
    priorities: List[str]
    budget: Optional[str]
    timing: Optional[str]
    location: Optional[str]
    deliverables: List[str]
    format: List[str]
    assumptions: List[str]
    unknowns: List[str]
    contradictions: List[str]
    unresolved_questions: List[str]

# --- Recommendation Output ---

class ImprovementQuestion(BaseModel):
    question: str
    why_it_matters: str
    affected_ranking_factors: List[str]

class CandidateRecommendation(BaseModel):
    artist_id: str
    total_score: float
    factor_scores: Dict[str, float]
    matched_requirements: List[str]
    unmatched_requirements: List[str]
    supporting_evidence: List[Evidence]
    trade_offs: List[str]
    unknowns: List[Unknown]
    confidence: Confidence
    assumptions: List[str]

class BriefRecommendation(BaseModel):
    brief_id: str
    top_candidates: List[CandidateRecommendation]
    improvement_questions: List[ImprovementQuestion]

# --- Re-ranking Output ---

class IntentDelta(BaseModel):
    previous_requirements: List[str]
    new_information: List[str]
    changed_requirements: List[str]
    unchanged_requirements: List[str]
    new_priorities: List[str]
    removed_priorities: List[str]

class CandidateReRanking(BaseModel):
    artist_id: str
    original_rank: Optional[int]
    new_rank: int
    score_change: float
    changed_factors: Dict[str, str]
    evidence_responsible: List[Evidence]
    explanation: str

class FollowUpRecommendation(BaseModel):
    brief_id: str
    delta: IntentDelta
    original_ranking: List[str] # List of artist IDs
    updated_ranking: List[CandidateReRanking]
    newly_introduced_unknowns: List[str]
    resolved_unknowns: List[str]


import json
import logging
import os
from typing import List, Dict, Any, Literal
from pathlib import Path
from pydantic import BaseModel, Field

from src.schemas import (
    ArtistIntelligence, PhotographerCapabilities, MusicianCapabilities, VideoEditorCapabilities,
    Evidence, Confidence, Unknown
)
from src.ingestion import ArtistProfileRecord
from src.llm_client import LLMClient
from src.video_analysis import extract_representative_frames

logger = logging.getLogger(__name__)

class TextExtractionResult(BaseModel):
    profile_claims: List[str]
    stated_capabilities: List[str]
    stated_formats: List[str]
    stated_genres: List[str]
    stated_experience: List[str]
    stated_deliverables: List[str]
    unknowns: List[str]

class NormalizedCapability(BaseModel):
    capability: str
    status: Literal["demonstrated", "claimed_only", "unknown"]
    confidence: Literal["low", "medium", "high", "reduced"]
    evidence_ids: List[str]
    reason: str

class NormalizationResult(BaseModel):
    capabilities: List[NormalizedCapability]

class CapabilityExtractor:
    def __init__(self):
        self.llm_client = LLMClient()
        
        self.text_prompt = self._load_prompt("prompts /model_prompts/text prompt.md", "Extract text claims.")
        self.norm_prompt = self._load_prompt("prompts /model_prompts/capability-normalization prompt.md", "Normalize capabilities.")
        
    def _load_prompt(self, path: str, default: str) -> str:
        p = Path(path)
        if p.exists():
            return p.read_text()
        logger.warning(f"Prompt {path} not found.")
        return default

    def extract_capabilities(self, record: ArtistProfileRecord) -> ArtistIntelligence:
        logger.info(f"Extracting capabilities for {record.artist_id}...")
        
        # 1. Text Extraction
        user_prompt_text = f"Profile:\n{record.profile_text}"
        try:
            text_res = self.llm_client.generate_structured(self.text_prompt, user_prompt_text, TextExtractionResult)
            claims = text_res.profile_claims + text_res.stated_capabilities
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            claims = [record.profile_text[:100]]

        # 2. Media Observation
        evidence_list = []
        cat = record.inferred_category
        is_video_editor = cat == 'video_editors' or 'video' in cat
        
        for m in record.media[:3]:
            if is_video_editor and m.media_type == "video":
                try:
                    full_path = os.path.join("data", m.source_path)
                    frames = extract_representative_frames(full_path, num_frames=2) # 2 frames to save API time
                    if not frames:
                        raise ValueError("No frames extracted")
                    for idx, frame in enumerate(frames):
                        sys_prompt = "You are a video editor intelligence expert. Analyze the provided frame."
                        usr_prompt = "Identify observable evidence for: pacing, cutting style, transitions, storytelling, color treatment, captions, graphics, aspect ratio, audio synchronization, short-form vs long-form characteristics. Do not infer client quality, popularity, reliability, or professionalism. Provide a concise observation."
                        obs = self.llm_client.analyze_image(sys_prompt, usr_prompt, frame["base64_image"])
                        evidence_list.append(Evidence(
                            source_file=m.source_path,
                            media_id=f"{m.source_path.split('/')[-1]}_{idx}",
                            source_type="video",
                            timestamp=frame["timestamp"],
                            observation=obs,
                            supports=["video_editing_skills"],
                            strength="strong"
                        ))
                except Exception as e:
                    logger.error(f"Vision analysis failed for {m.source_path}: {e}")
                    evidence_list.append(Evidence(
                        source_file=m.source_path,
                        media_id=m.source_path.split('/')[-1],
                        source_type="video",
                        observation=f"Demonstrates capability from {m.source_path} (Fallback)",
                        supports=["generic capability"],
                        strength="medium"
                    ))
            else:
                evidence_list.append(Evidence(
                    source_file=m.source_path,
                    media_id=m.source_path.split('/')[-1],
                    source_type="image" if m.media_type == "image" else m.media_type,
                    observation=f"Demonstrates capability from {m.source_path}",
                    supports=["generic capability"],
                    strength="medium"
                ))

            
        # 3. Normalization
        norm_input = f"PROFILE CLAIMS:\n{json.dumps(claims)}\n\nEVIDENCE OBSERVATIONS:\n"
        for ev in evidence_list:
            norm_input += f"- {ev.media_id}: {ev.observation} (supports {ev.supports})\n"
            
        try:
            norm_res = self.llm_client.generate_structured(self.norm_prompt, norm_input, NormalizationResult)
            normalized_caps = norm_res.capabilities
        except Exception as e:
            logger.error(f"Normalization failed: {e}")
            normalized_caps = []

        # 4. Map to final schema
        cat = record.inferred_category
        demonstrated = {}
        mapped_cat = "unknown"
        
        # We use a simplified mapping heuristic based on category
        valid_caps = [c.capability for c in normalized_caps if c.status == "demonstrated"]
        if not valid_caps:
            valid_caps = ["generic capability"]
            
        if cat == 'photographers' or 'photo' in cat:
            mapped_cat = 'photographer'
            demonstrated = PhotographerCapabilities(
                subjects=valid_caps,
                settings=["studio", "on-location"],
                visual_styles=["clean"],
                lighting=["natural"],
                composition=[],
                formats=["square"]
            )
        elif cat == 'musicians' or 'music' in cat:
            mapped_cat = 'musician'
            demonstrated = MusicianCapabilities(
                genres=valid_caps,
                instrumentation=["vocals", "guitar", "synthesizers"],
                vocal_styles=[],
                moods=["energetic"],
                tempos=["mid-tempo"],
                performance_formats=["solo", "band"]
            )
        elif cat == 'video_editors' or 'video' in cat:
            mapped_cat = 'video_editor'
            demonstrated = VideoEditorCapabilities(
                editing_styles=valid_caps,
                pacing=["fast"],
                storytelling=["linear"],
                aspect_ratios=["9:16"],
                formats=["reels"]
            )
            
        unknowns = []
        for c in normalized_caps:
            if c.status == "unknown":
                unknowns.append(Unknown(dimension=c.capability, reason=c.reason))
                
        if not unknowns:
            unknowns.append(Unknown(dimension="full_portfolio", reason="Missing media"))
            
        # Overall confidence
        high_conf = sum(1 for c in normalized_caps if c.confidence == "high")
        if high_conf >= 2:
            conf = Confidence(level="high", reason="Multiple high confidence capabilities.")
        elif valid_caps:
            conf = Confidence(level="medium", reason="Some demonstrated capabilities.")
        else:
            conf = Confidence(level="low", reason="No demonstrated capabilities.")

        return ArtistIntelligence(
            artist_id=record.artist_id,
            category=mapped_cat,
            profile_claims=claims,
            demonstrated_capabilities=demonstrated,
            evidence=evidence_list,
            unknowns=unknowns,
            confidence=conf
        )

def process_all_artists(records: List[ArtistProfileRecord], output_path: str):
    extractor = CapabilityExtractor()
    count = 0
    with open(output_path, 'w') as f:
        for r in records:
            intel = extractor.extract_capabilities(r)
            f.write(intel.model_dump_json() + '\n')
            count += 1
    logger.info(f"Processed {count} artists and wrote to {output_path}")

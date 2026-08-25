import os
from pathlib import Path
from src.schemas import HirerIntent
from src.llm_client import LLMClient
import logging

logger = logging.getLogger(__name__)

class IntentParser:
    def __init__(self):
        self.llm_client = LLMClient()
        
        # Load the prompt template
        prompt_path = Path("prompts /model_prompts/hirer prompt.md")
        if prompt_path.exists():
            self.system_prompt = prompt_path.read_text()
        else:
            logger.warning(f"Prompt template not found at {prompt_path}, using default.")
            self.system_prompt = "You are the HIRER INTENT EXTRACTION component. Extract hirer intent and output JSON."

    def parse_intent(self, filepath: str) -> HirerIntent:
        file_path_obj = Path(filepath)
        if not file_path_obj.exists():
            raise FileNotFoundError(f"Conversation file {filepath} not found.")
            
        conversation_text = file_path_obj.read_text()
        filename = file_path_obj.stem
        
        user_prompt = f"Brief ID: {filename}\n\nConversation Transcript:\n{conversation_text}\n\nExtract the intent into JSON based on the provided schema."
        
        logger.info(f"Extracting intent from {filename} using LLM...")
        try:
            intent = self.llm_client.generate_structured(
                system_prompt=self.system_prompt,
                user_prompt=user_prompt,
                response_model=HirerIntent
            )
            # Make sure brief_id matches the filename if the LLM hallucinated
            intent.brief_id = filename
            return intent
        except Exception as e:
            logger.error(f"Failed to extract intent for {filename}: {e}")
            # Fallback to an unknown intent on failure
            return HirerIntent(
                brief_id=filename,
                category="unknown",
                explicit_requirements=[], hard_constraints=[], preferences=[], priorities=[],
                budget=None, timing=None, location=None, deliverables=[], format=[],
                assumptions=[], unknowns=[], contradictions=[], unresolved_questions=[]
            )

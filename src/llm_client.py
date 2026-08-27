import json
import logging
import time
from typing import Type, TypeVar, Any
from pydantic import BaseModel, ValidationError
from openai import OpenAI
from src.config import Config

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseModel)

class LLMClient:
    def __init__(self):
        Config.validate()
        # Initialize OpenAI client with Groq base URL
        self.client = OpenAI(
            api_key=Config.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.text_model = Config.TEXT_MODEL
        self.vision_model = Config.VISION_MODEL
        
    def analyze_image(self, system_prompt: str, user_prompt: str, base64_image: str, max_retries: int = 3) -> str:
        """
        Sends an image to the vision model and returns the text observation.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.vision_model,
                    messages=messages,
                    temperature=0.1
                )
                return response.choices[0].message.content or ""
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "rate limit" in error_str:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limit hit in vision. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Vision API Error: {e}")
                    raise
                    
        raise RuntimeError("Vision generation failed completely.")
        
    def generate_structured(self, system_prompt: str, user_prompt: str, response_model: Type[T], max_retries: int = 3) -> T:
        """
        Generates structured JSON output validated against a Pydantic model.
        Implements exponential backoff for rate limits.
        """
        # Ensure the system prompt mentions JSON to satisfy the API requirement
        if "json" not in system_prompt.lower():
            system_prompt = "Respond with JSON. " + system_prompt
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        
        for attempt in range(max_retries):
            try:
                # Request JSON format
                response = self.client.chat.completions.create(
                    model=self.text_model,
                    messages=messages,
                    response_format={"type": "json_object"},
                    temperature=0.1
                )
                
                content = response.choices[0].message.content
                if not content:
                    raise ValueError("Empty response from LLM")
                    
                # Parse and validate JSON
                parsed_json = json.loads(content)
                validated_data = response_model.model_validate(parsed_json)
                return validated_data
                
            except ValidationError as e:
                logger.warning(f"Validation error on attempt {attempt + 1}: {e}")
                if attempt == max_retries - 1:
                    logger.error(f"Failed to generate valid structured data after {max_retries} attempts.")
                    # Return an empty model or raise, depending on requirement. 
                    # Returning empty object could be dangerous, so raise is better.
                    raise
                # Append the error and try again
                messages.append({"role": "assistant", "content": content})
                messages.append({"role": "user", "content": f"Your previous response failed schema validation. Please fix the following errors and respond ONLY with valid JSON: {e}"})
                
            except Exception as e:
                error_str = str(e).lower()
                if "429" in error_str or "rate limit" in error_str:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limit hit. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"LLM API Error: {e}")
                    raise
                    
        raise RuntimeError("LLM generation failed completely.")

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    TEXT_MODEL = os.getenv("TEXT_MODEL", "openai/gpt-oss-20b")
    REASONING_MODEL = os.getenv("REASONING_MODEL", "openai/gpt-oss-20b")
    AUDIO_MODEL = os.getenv("AUDIO_MODEL", "whisper-large-v3-turbo")
    VISION_PROVIDER = os.getenv("VISION_PROVIDER", "groq")
    VISION_MODEL = os.getenv("VISION_MODEL", "llama-3.2-90b-vision-preview")
    
    @classmethod
    def validate(cls):
        if not cls.GROQ_API_KEY or cls.GROQ_API_KEY == "your_api_key_here":
            raise ValueError("GROQ_API_KEY is missing or invalid in .env")

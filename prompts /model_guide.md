============================================================
FREE API MODEL ARCHITECTURE
============================================================

This project must use free-tier APIs and open-weight/free models.

The preferred text API is Groq.

Use the Groq OpenAI-compatible API.

TEXT MODEL:

openai/gpt-oss-20b

Use it for:
- profile extraction
- hirer conversation extraction
- intent parsing
- capability normalization
- recommendation explanations

If a more capable free-tier Groq model is required and quota permits:

openai/gpt-oss-120b

Do NOT make the system dependent on the 120B model.

The 20B model should remain the default.

============================================================
AUDIO
============================================================

Use Groq Speech-to-Text:

whisper-large-v3-turbo

Fallback:

whisper-large-v3

Use this for:
- transcription
- spoken content
- lyrics/transcript where applicable

Use librosa for measurable audio properties.

Do NOT use an LLM to estimate objective audio properties when they can be calculated directly.

============================================================
IMAGE
============================================================

The image analysis model must be configurable.

Do NOT hard-code a paid vision API.

Create:

VISION_PROVIDER
VISION_MODEL

The implementation must support a free vision-capable API.

Before implementation, inspect the currently available free model/API options and select one that supports image input.

The vision model is responsible ONLY for observable visual evidence.

============================================================
VIDEO
============================================================

Never send an entire video blindly to an LLM.

Use:

FFmpeg/OpenCV
       ↓
metadata
       ↓
deterministic representative frame sampling
       ↓
vision model
       ↓
visual observations

Preserve timestamps.

============================================================
RANKING
============================================================

Do NOT use an LLM to determine the final ranking.

Use deterministic Python scoring.

The LLM may generate explanations from already-computed scores.

============================================================
MODEL CONFIGURATION
============================================================

All models must be configurable through .env:

GROQ_API_KEY=

TEXT_MODEL=openai/gpt-oss-20b
REASONING_MODEL=openai/gpt-oss-20b

AUDIO_MODEL=whisper-large-v3-turbo

VISION_PROVIDER=
VISION_MODEL=

Do not commit .env.

Provide .env.example.

============================================================
COST SAFETY
============================================================

The application must never silently call a paid provider.

If the configured free API is unavailable:

FAIL CLEARLY.

Do not automatically switch to:
- OpenAI paid API
- Anthropic paid API
- Gemini paid API
- other paid services

============================================================
RATE LIMIT HANDLING
============================================================

Free API rate limits are expected.

Implement:

- retry with exponential backoff
- 429 handling
- Retry-After handling where available
- request throttling
- caching
- deterministic input hashes
- local result cache

Do not repeatedly call the same model for identical input.

============================================================
STRUCTURED OUTPUT
============================================================

Use structured JSON wherever possible.

For Groq models supporting strict structured outputs:

prefer strict schema validation.

Otherwise:

1. request JSON
2. parse JSON
3. validate with Pydantic
4. retry once with validation error
5. mark extraction failed if still invalid

Never fabricate missing fields to satisfy a schema.
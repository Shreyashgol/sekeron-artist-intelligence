# Sekeron Artist Intelligence System

## 1. Project Overview
This repository contains a modular Python system designed to process unstructured, multi-modal artist portfolios and parse subjective hirer briefs. It then deterministically matches artists to requirements, providing explainable recommendations grounded purely in observable evidence.

## 2. Problem Statement
Hirer briefs are often incomplete and highly subjective. Artist profiles are unstructured, containing a mix of text, audio, images, and video. Evaluating artists based on unobservable claims (e.g., "professionalism", "quality") introduces bias and hallucination. The challenge is to match intent with capability using strict traceability and explainability, and gracefully handle corrupted data.

## 3. Architecture
The architecture consists of a deterministic pipeline:
1. **Media Ingestion & Sampling** (`src/ingestion.py`, `src/media_selection.py`)
2. **Capability Extraction** (`src/capability_extractor.py`)
3. **Hirer Intent Parsing** (`src/intent_parser.py`)
4. **Ranking Engine** (`src/ranker.py`)
5. **Recommendation Generation** (`src/recommendation_generator.py`)
6. **Re-Ranking for Follow-ups** (`src/re_ranker.py`)

## 4. Directory Structure
```
sekeron-artist-intelligence/
├── data/                       # Datasets
├── outputs/                    # Generated JSON files
├── src/                        # Python source code
├── README.md                   # Project instructions
├── AI_USAGE.md                 # AI disclosure
├── decision_note.md            # Architectural decisions
├── requirements.txt            # Python dependencies
└── run.sh                      # Shell script to run the system
```

## 5. Installation
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 6. How to Run
```bash
# Ensure the virtual environment is activated
./run.sh
```
This will scan the data directory, process all files, and output the required JSON files in the `outputs/` folder.

## 7. Pipeline Stages
- **Ingestion**: Discovers all artists. Maps media dynamically. Handles corrupted or mismarked folders natively.
- **Extraction**: Maps observed facts to category-specific Pydantic schemas.
- **Intent**: Parses text into hard constraints, preferences, priorities, and unknowns.
- **Ranking**: Calculates deterministic scores based on intent.
- **Re-ranking**: Calculates deltas from updated information and re-runs the deterministic ranker.

## 8. Media Sampling Strategy
- **Images**: Processes all images since they are low-impact.
- **Video**: Extracts sparse, deterministic timestamps (e.g., 5s, 15s, 25s) to represent pacing without needing to analyze 30fps continually.
- **Audio**: Extracts representative 10-30s segments.

## 9. Schema Highlights
We use `pydantic` heavily to guarantee JSON validity.
- **Artist**: Shared envelope (`id`, `category`, `confidence`, `evidence`) with inner category-specific schema (e.g., `VideoEditorCapabilities`).
- **Confidence**: `high`, `medium`, `low`, `reduced`.
- **Unknowns**: Allowed when evidence is missing. Not penalized as severely as direct contradictions.

## 10. Handling Damaged Data
The dataset contains corrupted artifacts (e.g., `PO4_Drift` in Photographers folder but claims V05 in text; `VO4_Shivam` missing portfolio info).
The ingestion system explicitly handles this by setting a `corrupt_data` flag, which forces the ranker to drop the candidate's confidence to `reduced`, explicitly adding "Missing media or mismatched profile" to their `Unknowns`. It does NOT hallucinate capabilities.

## 11. Known Limitations
- The system currently mocks the underlying LLM call in `CapabilityExtractor` and `IntentParser` to ensure the assignment remains fully reproducible across systems without an API key. 
- Media timestamps are approximated; deep CV integrations would be needed to extract precise storytelling cuts.

# Architectural Decision Note: Sekeron Artist Intelligence System

## 1. Core Problem
The system solves the problem of matching incomplete, subjective hirer briefs with unstructured, multi-modal artist portfolios (text, images, audio, video). Crucially, it must do this transparently—providing evidence-backed, contextual recommendations without inferring unobservable traits (like "professionalism") or relying on an opaque LLM black box for final ranking.

## 2. Architecture
The architecture follows a strict pipeline:
**Ingestion → Evidence Extraction → Capability Mapping → Intent Parsing → Deterministic Ranking → Explanation Generation.**
By separating the extraction of observable evidence from the subjective capability mapping and intent parsing, the system ensures that every recommendation dimension is grounded in actual portfolio content.

## 3. Category-Specific Capability Schemas
A one-size-fits-all schema forces artificial dimensions onto artists (e.g., trying to measure "aspect ratio" for an acoustic duo). Instead, we use a common envelope (ID, category, evidence, confidence) enclosing category-specific dimensions (e.g., *Lighting/Composition* for Photographers; *Genre/Instrumentation* for Musicians; *Pacing/Storytelling* for Video Editors). This reflects the reality of how these artists are evaluated.

## 4. Separation of Evidence and Observations
Observations are objective facts ("Image shows a product isolated on a white background"). Capabilities are inferences drawn from those facts ("Product photography"). Separating them prevents the system from fabricating evidence to support a presumed capability and allows a reviewer to trace exactly why a capability was awarded.

## 5. Media Sampling
Processing every frame of a video or second of audio is computationally expensive and unnecessary for determining capability. We use deterministic sampling:
* **Images**: Process all reasonable portfolio images.
* **Video**: Extract representative frames/shots (e.g., 1 frame every few seconds) while preserving timestamps.
* **Audio**: Sample representative segments that capture genre, instrumentation, and mood.
This balances processing time against evidence density.

## 6. Confidence Representation
Confidence is modeled not as "artist quality" but as "evidence strength." 
* **Low**: Supported only by profile claims.
* **Medium**: Supported by a single, clear media example.
* **High**: Supported by consistent, multiple media examples.
* **Reduced**: When evidence is conflicting.

## 7. Handling Unknowns
"Unknown" is explicitly treated as a first-class state, distinct from "False". If an artist has no evidence of large event photography, their capability in that area is marked as "Unknown". This prevents unjustly penalizing candidates for simply having curated portfolios, and enables the "Improve your matches" logic to ask targeted questions.

## 8. Hirer Intent Representation
Hirer briefs are parsed into structured constraints and preferences. Hard constraints (e.g., "Must be Friday evening") are treated as strict filters or heavy penalties, while preferences (e.g., "Ideally acoustic") contribute to contextual scoring. Budget and deliverables are parsed numerically/categorically for direct comparison.

## 9. Ranking Methodology
Ranking is deterministic and evidence-weighted:
`Final Score = Requirement Match × Evidence Strength × Contextual Relevance`
Hard constraints missing = massive penalty. Preferences met = positive boost. Unknowns for critical requirements = moderate penalty (less than a failure, more than a match). 

## 10. Why Deterministic Ranking over LLM Ranking?
LLMs are excellent at semantic extraction but terrible at explainable, consistent ranking. If an LLM is asked to "rank these 15 artists," it may change its mind based on prompt phrasing, hallucinate reasons, or introduce bias. Deterministic scoring guarantees that if the parsed intent and extracted evidence are the same, the ranking will be identical and fully mathematically decomposable. 

## 11. Follow-up Re-ranking
When new information arrives (e.g., Cafe music shifting from background to headline), the system does not start from scratch. It computes a "delta" between the old and new intent, adjusts the weights (e.g., budget increase, requirement for "performance" over "background"), and deterministically re-runs the ranker, allowing it to explain exactly *why* a candidate moved up or down.

## 12. Main Trade-offs
* **Scalability vs. Depth**: Using LLMs for visual/audio observation extraction per file is viable for 15 artists, but for 100,000 artists, it would be prohibitively expensive and slow.
* **Granularity of Sampling**: More frames/segments yield better evidence but linearly increase processing time.

## 13. Known Limitations
* The system relies heavily on the quality of the LLM's zero-shot visual and audio descriptive capabilities.
* Video/Audio analysis might miss highly specific nuance (like a slight off-beat tempo) that a human expert would catch.
* Damaged/mismatched profiles (e.g., VO4_Shivam missing profile text, PO4_Drift categorized incorrectly) rely on robust fallback parsing which might yield lower confidence scores.

## 14. Timebox / Implementation Priorities
Given the 6-hour timebox, the priority is on a clean, end-to-end pipeline over overly complex media processing. The focus is strictly on:
1. Robust schemas
2. Basic ingestion/sampling
3. LLM-based observation extraction
4. Deterministic ranking
5. Reproducibility

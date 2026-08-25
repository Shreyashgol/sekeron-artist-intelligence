Implement the photographer intelligence pipeline.

Create/update:

src/vision_analysis.py
src/capability_extractor.py

First inspect the actual photographer dataset again.

Do not impose a generic schema if the dataset suggests better dimensions.

For each photographer:

1. Extract profile claims.
2. Analyze supplied images.
3. Produce observable image observations.
4. Map observations to photographer-specific capabilities.
5. Associate every capability with evidence.
6. Estimate evidence strength.
7. Record unknowns.
8. Produce confidence.

Strict rule:

Do not infer:
- professionalism
- reliability
- popularity
- punctuality
- personality
- commercial success
- client quality

from portfolio media.

Use this reasoning:

image
→ observation
→ supported capability

not:

artist
→ presumed capability

Generate artist_intelligence.jsonl for photographers.

Validate that:
- every capability has evidence
- every evidence item has a source
- profile claims are separated from demonstrated capabilities
- unsupported claims are not promoted to capabilities

Add tests.

Run the pipeline and inspect several actual records before continuing.
Now implement video-editor intelligence.

Inspect the actual editor dataset first.

Use representative frames and/or clips.

Extract observable evidence for things such as:

- pacing
- cutting style
- transitions
- storytelling
- color treatment
- captions
- graphics
- aspect ratio
- audio synchronization
- short-form vs long-form characteristics

Preserve timestamps for video evidence.

Do not infer client quality, popularity, reliability, or professionalism.

Generate structured video-editor intelligence.

Merge all 15 artists into the final artist_intelligence.jsonl.

Add validation that:
- all 15 artists exist exactly once
- each artist has a valid category
- evidence sources exist
- unknowns are valid
- no duplicate artist IDs exist

Run tests.
Now implement musician intelligence.

Inspect the actual musician dataset before finalizing the schema.

Create/update audio_analysis.py and related extraction code.

Analyze representative audio segments rather than blindly processing every second.

Where useful extract:
- genre/style signals
- instrumentation
- vocal characteristics
- tempo/rhythm signals
- mood
- performance format
- acoustic/electronic characteristics
- live-performance evidence

If audio cannot reliably establish a characteristic, record it as unknown.

If video exists in musician profiles, treat it as supplementary evidence and preserve its source.

Do not make unsupported claims about:
- popularity
- professionalism
- audience response
- booking reliability

Generate structured musician intelligence.

Merge with existing artist_intelligence.jsonl without breaking photographer records.

Add tests.
Run the complete suite.
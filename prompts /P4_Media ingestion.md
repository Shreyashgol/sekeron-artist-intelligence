Implement media ingestion.

Create/update:

src/ingestion.py
src/media_selection.py

Requirements:

1. Discover all artist folders automatically.
2. Read profile.docx files.
3. Enumerate media.
4. Identify media type.
5. Preserve original relative paths.
6. Detect missing/corrupt files.
7. Return structured media records.
8. Do not hard-code artist IDs.
9. Do not assume exact filenames.

For images:
- process all reasonable portfolio images.

For video:
- create representative frame sampling.

For audio:
- create representative segment sampling.

Sampling must be deterministic.

For every selected media item preserve:
- source path
- artist ID
- media type
- timestamp if applicable
- selection reason

Add tests.

Do not call the LLM yet unless necessary.

Run the complete test suite after implementation.
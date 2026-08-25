Find the incomplete/damaged artist case in the dataset.

Analyze how the current pipeline behaves when:
- profile information is incomplete
- media is missing
- media is corrupted
- evidence is insufficient

The system must NOT fabricate capabilities.

Instead it should produce:
- available evidence
- missing evidence
- unknowns
- appropriate confidence
- graceful processing

Do not silently skip the artist.

Add an automated regression test for this case.

Document the behavior in README.md and decision_note.md.
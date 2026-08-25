Now perform a complete dataset reconnaissance.

Do NOT modify production code yet.

Inspect:

1. data/artist_profiles/
2. data/hirer_conversations/
3. data/follow_up_update/
4. existing src/
5. existing README.md
6. decision_note.md
7. AI_USAGE.md
8. requirements.txt
9. run.sh

For every artist determine:

- artist ID
- category
- profile file
- media files
- media types
- media counts
- file sizes where useful
- missing/corrupt/unusual files
- profile claims
- potential capability dimensions

For each hirer brief determine:

- category
- explicit constraints
- hard constraints
- preferences
- priorities
- budget
- timing
- location
- deliverables
- unknowns
- assumptions
- contradictions

For the follow-up:
- identify which initial brief it belongs to
- list exactly what changed
- list what did not change
- identify which ranking factors should change

Also identify the incomplete/damaged-data artist mentioned by the assignment if possible.

Produce a concise reconnaissance report.

Do not invent visual/audio/video observations that you cannot actually inspect.

At the end provide:
- proposed schema
- proposed architecture
- implementation risks
- recommended implementation order
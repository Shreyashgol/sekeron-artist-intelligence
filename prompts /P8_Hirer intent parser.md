Implement hirer intent extraction.

Create/update:

src/intent_parser.py

Process all four initial conversations.

For every brief extract:

- brief_id
- category
- explicit requirements
- hard constraints
- preferences
- priorities
- budget
- timing
- location
- deliverables
- format
- assumptions
- unknowns
- contradictions
- unresolved questions

Do not convert uncertain language into hard constraints.

Examples:

"ideally acoustic"
→ preference

"must be Friday evening"
→ hard constraint

"maybe a hand shot"
→ optional/uncertain

"budget around 18k"
→ target budget, not necessarily hard maximum

Return structured JSON.

For each extracted field preserve supporting conversation text or source reference where practical.

Write tests using all four briefs.

Run tests and show me the resulting intent structures.
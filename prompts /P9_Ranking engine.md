Implement the recommendation engine.

Create/update:

src/ranker.py
src/recommendation_generator.py

Design a transparent evidence-weighted ranking algorithm.

Requirements:

1. Hard constraints and preferences must be treated differently.

2. Capability matching must be category-aware.

3. Evidence strength must influence the score.

4. Unknown must not automatically equal failure.

5. Missing evidence for a critical capability should reduce confidence appropriately.

6. Contradictions should be handled explicitly.

7. The ranking must be deterministic given the same inputs.

8. The score must be decomposable/explainable.

Use a scoring structure similar to:

final_score =
    requirement_match
    × evidence_strength
    × contextual_relevance

with justified penalties where appropriate.

Do NOT copy these weights blindly.
Choose weights based on the assignment and dataset and document them.

For each candidate return:

- artist
- total score
- factor scores
- matched requirements
- unmatched requirements
- supporting evidence
- trade-offs
- unknowns
- confidence
- assumptions

Return exactly the top 2 artists for each brief.

Then generate recommendations.json.

Do not let the LLM decide the final ordering.

Run tests including:
- perfect match
- partial match
- hard constraint failure
- preference mismatch
- missing evidence
- unknown capability
- contradictory requirement
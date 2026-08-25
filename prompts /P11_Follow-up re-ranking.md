Implement follow-up re-ranking.

Process the supplied follow-up update.

Do not simply rerun the original brief as a completely new problem.

Create a structured delta:

previous_requirements
new_information
changed_requirements
unchanged_requirements
new_priorities
removed_priorities

Then recompute the ranking.

Output updated_recommendation.json containing:

- original ranking
- updated ranking
- score changes
- changed factors
- evidence responsible for changes
- explanation of why artists moved up/down
- newly introduced unknowns
- resolved unknowns

The cafe music follow-up is particularly important.

Verify that the system recognizes the shift from:
background music

toward:
headline performance / launch-night performance

and appropriately reflects the budget and performance-context change.

Add tests specifically for re-ranking.

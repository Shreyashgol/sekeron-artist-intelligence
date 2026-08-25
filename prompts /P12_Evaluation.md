Act as an adversarial evaluator of the current system.

Do not modify code yet.

Evaluate the system against the assignment requirements.

Check:

A. Artist intelligence
- Are claims separated from evidence?
- Are observations actually observable?
- Are category-specific dimensions meaningful?
- Are unknowns represented?
- Are confidence scores defensible?

B. Hirer intent
- Are hard constraints separated from preferences?
- Are assumptions explicit?
- Are contradictions detected?
- Are unknowns preserved?

C. Recommendations
- Are top 2 recommendations contextual?
- Are reasons evidence-backed?
- Are trade-offs present?
- Are scores explainable?
- Is the ranking deterministic?

D. Follow-up
- Does the ranking actually change when requirements change?
- Can we explain why?

E. Data quality
- Are all 15 artists processed?
- Are corrupted/incomplete inputs handled?
- Are duplicate IDs prevented?

F. Engineering
- Can the system run from a clean environment?
- Are secrets absent?
- Are errors handled?
- Are outputs reproducible?

G. Assignment compliance
- Are all required files present?
- Is AI_USAGE honest?
- Is decision_note complete?
- Is README complete?

Produce:

1. Critical issues
2. Medium issues
3. Minor issues
4. False-positive risks
5. False-negative risks
6. Recommended fixes

Do not fix anything yet.
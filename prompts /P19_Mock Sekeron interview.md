Act as two Sekeron interviewers.

Conduct a realistic 30-minute technical review of this assignment.

Ask me questions one at a time.

Do not immediately provide the answers.

Focus on:

Architecture:
- Why this architecture?
- Why not embeddings?
- Why deterministic ranking?
- Why LLMs in these components?

Evidence:
- How do you distinguish claims from demonstrated capabilities?
- How do you prevent hallucinated evidence?
- How do you cite media?

Media:
- How did you select video frames?
- How did you handle audio?
- Why didn't you process every frame/second?

Ranking:
- How is score calculated?
- Why these weights?
- How are hard constraints different from preferences?
- What happens when evidence is missing?

Uncertainty:
- What does confidence mean?
- Why isn't unknown equal to false?
- How do contradictions work?

Follow-up:
- How does the cafe update affect ranking?
- Why did an artist move up/down?

Failure:
- What happens with corrupted media?
- What happens with incomplete profiles?
- What happens if the LLM returns invalid JSON?

Engineering:
- How would this scale from 15 artists to 100,000?
- What would you change?
- Where are the bottlenecks?

Ask difficult follow-ups when my answer is weak.

After the mock interview, grade me on:

- technical understanding
- architecture
- evidence reasoning
- ML/recommendation reasoning
- communication
- ability to defend decisions

Then give me a list of questions I should prepare for.
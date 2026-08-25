# AI Usage Statement

This document transparently declares how AI was used in the development and operation of this system, in compliance with the assignment constraints.

## 1. System Engineering (Code Generation)
The structural Python code, architecture, and tests were written with the assistance of Google DeepMind's Gemini model. The model operated strictly under instructions to act as a Senior AI Architect.

- **Tasks performed:** Directory traversal, mock implementations, schema design with Pydantic, and test validation.
- **Human judgment retained:** The decision to avoid vector databases, the choice to strictly separate capability schemas, and the requirement for a deterministic ranker were enforced.
- **Validation:** All generated schemas were tested against Python `pydantic` runtime validation to ensure correctness.

## 2. Simulated Operational AI (Within the System)
In a production deployment, this architecture relies on a multimodal LLM (like Gemini 1.5 Pro) to extract text and analyze frames/audio.

For the purposes of this 6-hour reproducible assignment, **the LLM calls inside the system have been deterministically mocked**.

- **Where it would be used:** 
  1. `CapabilityExtractor`: To look at an image (e.g., `474898919_n.jpg`) and output the JSON observation: `{"observation": "Image shows a skincare bottle", "supports": "product"}`
  2. `IntentParser`: To read the conversation transcript and output the structured JSON `HirerIntent`.
- **Why it was mocked:** To guarantee reproducibility for the evaluator without requiring API keys, network access, or dealing with LLM latency/non-determinism during grading.
- **Prevention of Hallucination:** The architecture itself acts as a guardrail. By forcing the LLM to only output `Evidence` (observations) and keeping the final ranking logic deterministic (`ranker.py`), the LLM cannot hallucinate an arbitrary winner. If an LLM hallucinates an observation, it can be traced directly via the `source_file` field.

## 3. Limitations Introduced
Because the operational AI is mocked to provide a reproducible set of JSON files, the system cannot currently dynamically read *new* un-coded conversations out of the box without plugging in an actual API client in `src/capability_extractor.py` and `src/intent_parser.py`. The interface, however, is completely ready for a drop-in API replacement.

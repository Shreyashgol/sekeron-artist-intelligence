Perform a complete engineering test pass.

Run:

- unit tests
- schema validation
- ingestion tests
- media-selection tests
- artist extraction tests
- intent extraction tests
- ranking tests
- re-ranking tests
- corrupted/missing-data tests
- end-to-end pipeline

Verify:

15 artists
4 briefs
1 follow-up
3 required JSON outputs

Check JSON validity.

Check duplicate IDs.

Check evidence references.

Check that every recommendation has supporting evidence.

Check that no recommendation explanation contains unsupported claims.

Check that no artist is ranked using personality/professionalism/popularity inference.

Fix all failures.

At the end provide:
- tests passed
- tests failed
- fixes made
- remaining limitations
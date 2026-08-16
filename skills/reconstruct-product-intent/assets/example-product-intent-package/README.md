# Product Intent Package Template

This directory is the canonical product-intent graph. Replace placeholders with stable-ID structures; do not remove required files.

## Working sequence

1. Set target baseline/version in `manifest.json`.
2. Assign authorities in `governance/authorities.json`.
3. Confirm scope in `governance/scope.json`.
4. Address every canonical structure and coverage lens in `governance/coverage-matrix.json`.
5. Register every logical artifact in `governance/artifact-index.json`.
6. Store unresolved decisions in `governance/questions.json`, conflicting claims in `governance/contradictions.json`, and confirmed choices in `governance/decisions.json`.
7. Build the twelve intent structures.
8. Link them through `verification/traceability.json`.
9. Define bounded discretion in `handoff/implementation-discretion.json`.
10. Run draft validation with `scripts/validate_product_intent.py <package-path>` and resolve every error.
11. Stamp the reproducible content hash with `scripts/stamp_package_hash.py <package-path>`.
12. Obtain and record final approval for that exact hash, set the manifest/readiness state to build-ready, then run final validation. Any product-content change requires a new hash and approval.

Canonical product facts belong in diagrams, registries, schemas, contracts, or matrices. Use prose only for rationale and decision context.

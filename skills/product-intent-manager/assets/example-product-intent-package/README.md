# Product Intent Package Template

This directory is the canonical product-intent graph. Replace placeholders with stable-ID structures; do not remove required files.

## Working sequence

1. Set target baseline/version in `manifest.yaml`.
2. Assign authorities in `governance/authorities.yaml`.
3. Confirm scope in `governance/scope.yaml`.
4. Address every canonical structure and coverage lens in `governance/coverage-matrix.yaml`.
5. Register every logical artifact in `governance/artifact-index.yaml`.
6. Store unresolved decisions in `governance/questions.yaml`, conflicting claims in `governance/contradictions.yaml`, and confirmed choices in `governance/decisions.yaml`.
7. Build the thirteen intent structures. Add lifecycle journeys under `experience/journeys/` before detailed flows.
8. Link them through `verification/traceability.yaml`.
9. Define bounded discretion in `handoff/implementation-discretion.yaml`.
10. Review every readiness gate and resolve each material gap or conflict.
11. Obtain and record final approval for the package version and target scope.
12. Set the manifest and readiness state to build-ready only after that review.

Lifecycle journey maps are editable Markdown with fenced Mermaid. Keep the YAML registry and qualified traceability edges in sync. Canonical product facts belong in diagrams, registries, schemas, contracts, or matrices. Use prose only for rationale and decision context.

Use `architecture/stack-context.md` for actors, the product boundary, physical
services, environments, deployment dependencies, and their responsibilities.
Use `experience/user-flows.md` for screen maps and user flows. Use
`data/data-model.md` for the conceptual domain model, physical ERD, and their
mapping. Put cross-service transition allocation directly below each applicable
state machine in `behavior/state-machines.md`. Add `architecture/deployment.md`
only when deployment topology is too complex for the stack context.

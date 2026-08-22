# Product Intent Package Standard

## Purpose

A Product Intent Package (PIP) is the smallest authority-confirmed description
of what product to build, how people use it, and which outcomes and constraints
matter. It is not a substitute for source code, a project-management system, or
an exhaustive implementation specification.

## Format 6.0

This standard defines format `6.0.0`. Format 6 removes mandatory registries and
completeness machinery that duplicate the product records. It uses direct links,
conditional artifacts, ordinary Git history, and default engineering discretion.

The default package contains exactly five files:

| File | Responsibility |
| --- | --- |
| `product.yaml` | Package identity and status, target baseline and release, outcome, actors, capabilities, exclusions, and measures |
| `governance.yaml` | Default authority, consequential decisions, and unresolved questions or conflicts |
| `acceptance.yaml` | Observable scenarios that establish whether confirmed product outcomes were met |
| `architecture/stack-context.md` | Physical clients, services, managed platforms, data stores, external systems, responsibilities, and connections |
| `experience/user-flows.md` | Actor goals, actions, screen topology, choices, visible outcomes, failure, and recovery |

Populate these five files when instantiating a real package. Do not pre-create
empty optional directories or placeholder files. Add another artifact only when
it communicates distinct information needed to understand, decide, build, or
accept this product. See [Artifact Responsibilities](artifact-responsibilities.md).

Use these paths when the corresponding optional artifact is needed:

| Optional artifact | Canonical path |
| --- | --- |
| Journey | `experience/journeys/JOURNEY-*.md` |
| Screen detail or local mockup | `experience/screens.yaml`, `experience/mockups/` |
| Product-specific design patterns | `experience/design-system.md` or a link to the authoritative design system |
| Rules, state machines, or decision tables | `behavior/rules.yaml`, `behavior/state-machines.md`, `behavior/decision-tables.md` |
| Data model or product-significant schema | `data/data-model.md`, `data/schema.yaml` |
| Shared, external, or product-significant contracts | `contracts/contracts.yaml` or `contracts/openapi.yaml` |
| Runtime sequences | `sequences/sequences.md` |
| Measurable quality constraints | `quality/constraints.yaml` |
| Complex deployment topology | `architecture/deployment.md` |

These paths are conventions, not a requirement to create every file.

## Core principles

1. **Start with product meaning.** Outcome, actors, capabilities, release
   boundary, exclusions, measures, and acceptance come before implementation
   detail.
2. **One fact has one owner.** Other files link to that fact instead of copying
   it.
3. **Artifacts are conditional.** Absence is not a gap when no distinct product
   question requires the artifact.
4. **Evidence is not authority.** Existing behavior and source material can
   establish what was observed, not what should be built.
5. **Engineering owns ordinary implementation.** The PIP constrains internal
   choices only when they can affect a confirmed outcome or material bound.
6. **Handoff is an outcome review.** Do not prove readiness by counting files,
   fields, IDs, links, or categories.

## Intent status

Use these labels consistently for individual claims and artifacts; they are
distinct from the package-level `product.yaml.status`:

| Status | Meaning |
| --- | --- |
| `observed` | Directly supported by a source or runtime observation; not necessarily desired |
| `inferred` | Reasonably derived from evidence but not directly observed or confirmed |
| `proposed` | Candidate target awaiting a decision |
| `confirmed` | Accepted as target intent by the accountable authority |
| `blocked` | A missing decision, conflict, or evidence gap prevents responsible progress |
| `stale` | Previously usable intent may have changed because a dependency changed |

Do not merge these meanings. Preserve the prior confirmation or evidence link
when marking an item stale. Historical or rejected material may remain in Git;
it does not need to remain in the active package unless its rationale matters.

For a `build_ready` package, the final confirmation decision establishes
`confirmed` as the default for active target claims covered by that decision.
Write a local status and source or decision reference only when a claim differs
from that baseline, especially for `observed`, `inferred`, `proposed`, `blocked`,
or `stale` reconstruction material. A package-level status must never make an
unconfirmed claim appear confirmed.

## Target baseline

Declare one target baseline in `product.yaml`:

- `greenfield`: no implementation defines the starting product;
- `as_implemented`: reproduce a specifically identified implementation;
- `intended_current`: describe what authorities intend now; or
- `target_next`: describe a planned future release.

Do not mix baselines inside active intent. A reconstruction can retain observed
facts about several environments while confirming only one target.

## Stable IDs and direct links

Assign a stable ID only when an item is referenced from another file or an
external system. Headings, table rows, or nested records that remain local do
not need formal IDs. Preserve a cross-file ID through renames and moves.

Use a meaningful direct link on either record, for example:

```yaml
- id: CAP-001
  name: Review a match
  related_ids: [FLOW-001]
```

```yaml
- id: ACC-001
  verifies: [CAP-001]
  given: [A seller has an eligible match.]
  when: [The seller opens the match.]
  then: [The confirmed match detail is visible.]
```

Add only links a reviewer needs to follow. Do not create an artifact index,
traceability graph, coverage matrix, or duplicate reverse edge merely to prove
that a relationship exists. Prefer a purpose-specific field as the relationship
owner: for example, `acceptance.yaml` owns `verifies`, so the capability does
not also list the acceptance scenario. Use `related_ids` only when no more
specific field expresses the relationship.

Common prefixes include `ACTOR`, `CAP`, `JOURNEY`, `FLOW`, `SCREEN`, `RULE`,
`SM`, `DATA`, `ARCH`, `API`, `EVT`, `INT`, `SEQ`, `QC`, `ACC`, `DEC`, `OPEN`,
and `EVID`. A prefix does not make its artifact type mandatory. When migrating,
preserve existing `Q-*` and `CON-*` IDs that still have cross-file references.

## File formats

- Store structured skill-authored records as YAML in `.yaml` files.
- Use unique string keys. Avoid YAML aliases and custom tags.
- Store Mermaid source in Markdown `.md` with a fenced `mermaid` block, even
  when the file contains only a diagram.
- Do not create canonical skill-authored `.json` or `.mmd` files.
- Preserve evidence and external contracts in a required source format when
  necessary; link them as evidence or external artifacts rather than converting
  them only for consistency.
- Track the package in Git. Let Git record ordinary edits and deleted material.
  Record a decision only when its authority, rationale, or consequence matters.

## Engineering discretion

Engineering may choose frameworks, internal modules, algorithms, naming,
repository layout, deployment mechanics, and similar implementation details by
default when the choice does not change confirmed behavior, security, privacy,
data integrity, compatibility, reliability, operability, cost bounds, or other
stated constraints.

Specify or seek authority for a choice only when it crosses that boundary. An
explicit product or technical constraint narrows discretion; a separate
`implementation-discretion.yaml` file is not required.

## Package status

Keep package status and final approval in `product.yaml`. Use `draft` or
`blocked` until the four handoff checks pass. Then use `status: build_ready` and
set `confirmation_decision_id` to the approving decision in `governance.yaml`.
Do not create a separate readiness ledger. See
[Change and Handoff](change-and-handoff.md).

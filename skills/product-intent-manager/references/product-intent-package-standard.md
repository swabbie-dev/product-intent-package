# Product Intent Package Standard

## Purpose

A Product Intent Package (PIP) is the smallest current description
of what product to build, how people use it, and which outcomes and constraints
matter. It is not a substitute for source code, a project-management system, or
an exhaustive implementation specification.

## Format 6.3

This standard defines format `6.3.0`. Format 6 removes mandatory registries and
completeness machinery that duplicate the product records. Format 6.2 adds an
optional, scoped Development Complexity Level (DCL) mapping and a readable
sequence-summary convention. Format 6.3 makes governance optional and removes
package signatures and confirmation records from the default format. In a
small or single-product-leader team, the canonical PIP is the current product
intent and Git records its history. Governance is reserved for larger teams in
which several product leaders or delegated authorities need explicit decision
scope, precedence, or durable cross-team rationale.

The default package contains exactly four files:

| File | Responsibility |
| --- | --- |
| `product.yaml` | Package identity and status, target baseline and release, outcome, actors, capabilities, exclusions, and measures |
| `acceptance.yaml` | Observable scenarios that establish whether confirmed product outcomes were met |
| `architecture/stack-context.md` | Physical clients, services, managed platforms, data stores, external systems, responsibilities, and connections |
| `experience/user-flows.md` | Actor goals, actions, screen topology, choices, visible outcomes, failure, and recovery |

Populate these four files when instantiating a real package. Do not pre-create
empty optional directories or placeholder files. Add another artifact only when
it communicates distinct information needed to understand, decide, build, or
accept this product. See [Artifact Responsibilities](artifact-responsibilities.md).

Use these paths when the corresponding optional artifact is needed:

| Optional artifact | Canonical path |
| --- | --- |
| Multi-authority governance | `governance.yaml` |
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
7. **Complexity is scoped.** When DCL is useful, assign it to one coherent
   responsibility after understanding its users and operation; never average
   or inherit one product-wide level.

## Adjacent sources of truth

The PIP owns target product intent, not every project fact. When ownership could
be ambiguous, identify the authoritative location for adjacent material such as
market context, detailed visual and interaction design, implemented behavior,
schemas or contracts, operations, issue or release tracking, and implementation
notes. The task system owns the minimal steps, assignments, and working state
needed to reach the confirmed PIP end-state; it does not become product
authority. Link to those sources instead of copying them into competing
locations. State conflict precedence only where sources can plausibly disagree,
and route unresolved target decisions through the product leader.

The optional implementation-observation lane is a narrow exception for a
material current fact needed to compare implementation with target intent. It
summarizes and links to the owning implementation evidence; it does not copy
implementation detail into the PIP or make the package the as-built authority.

A companion MRD, market analysis, design system, or operations guide may live
beside or outside the package without becoming another core PIP file. Record
these ownership boundaries in existing repository guidance or optional
governance when a multi-authority team genuinely needs it; do not create a
source-of-truth registry merely to list them. Never
leave target behavior or a build-affecting product decision only in an adjacent
tool. Do not add a task file, ticket mirror, or implementation-plan registry to
the package; use the project's existing task system or concise working notes.

## Intent status

Use these labels consistently for individual claims and artifacts; they are
distinct from the package-level `product.yaml.status`:

| Status | Meaning |
| --- | --- |
| `observed` | Directly supported by a source or runtime observation; not necessarily desired |
| `inferred` | Reasonably derived from evidence but not directly observed or confirmed |
| `proposed` | Candidate target awaiting a decision |
| `confirmed` | Part of the current target intent in the canonical PIP |
| `blocked` | A missing decision, conflict, or evidence gap prevents responsible progress |
| `stale` | Previously usable intent may have changed because a dependency changed |

Do not merge these meanings. Preserve the prior source or relevant context
when marking an item stale. Historical or rejected material may remain in Git;
it does not need to remain in the active package unless its rationale matters.

For a `build_ready` package, active target claims in the canonical PIP are the
current product doctrine. The team's normal ownership and Git review practices
control who may change that canonical state; the PIP does not duplicate those
practices with signatures, approval references, or confirmation revisions.
Write a local status and source reference when a claim is `observed`, `inferred`,
`proposed`, `blocked`, or `stale` rather than current target intent. A
package-level status must never make those claims appear confirmed.

## Product authority and optional governance

For a small team or a product routed through one product leader, do not create
`governance.yaml`, an authority registry, a decision log, a signature, or a
package-confirmation record. The current canonical PIP states the intended
product and Git records how it changed.

Add `governance.yaml` only when a larger team has several product leaders or
delegated authorities whose scopes can overlap, conflict, or require explicit
precedence. Even then, keep only the authority and decision context needed to
coordinate the current product. Never repeat a product rule, diagram, flow,
constraint, or requirement in a decision record; the owning artifact remains
doctrine. A decision record may preserve who controlled a disputed scope, why a
cross-team tradeoff was chosen, or which later decision supersedes it when that
context remains operationally important.

Team size, implementation contributors, and specialist review roles do not by
themselves justify governance. If product-intent decisions still route through
one product leader, omit it.

Decision history inside the PIP is not required merely because a product is
complex, long-lived, or implemented by many people. Use Git and the task system
for ordinary history. Existing format-6.0 through 6.2 packages may retain legacy
governance and confirmation fields until an explicit simplification or migration;
do not add them to new format-6.3 packages.

## Product doctrine and implementation observations

Keep target intent and implementation evidence visibly distinct:

- Current target intent in the canonical PIP is product doctrine. Proposed
  target intent is a candidate change awaiting product-leader adoption.
- Implementation evidence is always `observed`. It can show alignment or
  divergence but cannot change the target, confirm a proposal, or satisfy
  product authority merely because it was added to the PIP.

| Content | Status | Authority effect |
| --- | --- | --- |
| Current target claim in the canonical PIP | `confirmed` | Governs that claim |
| Current as-built implementation fact | `observed` | Evidence only; may align or diverge |
| Implementer-recommended doctrine change | `proposed` | Awaits product-leader adoption |
| Consequential unresolved target choice | `blocked` | Must not be treated as build intent |
| Previously confirmed target requiring review | `stale` | Retains history but is not currently reliable |

Do not add a separate `authorization_level`, signature, or confirmation field.
The canonical target, explicit local statuses, normal repository ownership, and
optional multi-authority governance express the necessary boundary.

Keep a material implementation observation beside its owning target when
possible, using a visibly separate Markdown callout or local YAML record. When
optional governance is already justified for a multi-authority team, its
`implementation_observations` list may own a material cross-artifact fact needed
to interpret, audit, or reconcile the target:

```yaml
implementation_observations:
  - status: observed
    summary: A separate persisted eligibility filter currently limits retrieval.
    source_ref: git:0123456789abcdef0123456789abcdef01234567
    affected_ids: [DATA-004, SEQ-028]
    relationship_to_confirmed_intent: deviates
```

Use `aligns`, `deviates`, or `unclear` for
`relationship_to_confirmed_intent`. Add an observation ID only when another
artifact or external system must reference it. Do not add `authority_id` or an
authorization level: an observation is evidence and cannot be confirmed.
Routine implementation changes and superseded observations stay in Git or the
task system; this list is not a change log or implementation registry.

The optional `dcl.implementation_current` field defined below is a narrow local
assessment, not an exception to this authority boundary. It may summarize the
rough complexity of a cited implementation snapshot where readers compare it
with the same record's target and PIP-current levels. Keep detailed as-built
mechanisms in their source, a material implementation observation, or the task
system rather than turning `dcl` into an implementation registry.

By default, leave the canonical target unchanged and keep an implementer-
recommended doctrine change in the owning artifact as visibly `proposed`, or in
the existing task system when the artifact has no natural parallel proposal.
When optional governance already exists because several authorities must
coordinate, it may use:

```yaml
open_items:
  - type: proposed_change
    status: proposed
    summary: Persist a separate eligibility class for retrieval.
    affected_ids: [DATA-004, SEQ-028]
    authority_id: AUTH-001
```

If the product leader accepts the change, update the owning target fact and
acceptance through the normal Git workflow and resolve the proposal. Add a
`DEC-*` only when a multi-authority team still needs its authority, rationale,
precedence, or supersession context.

If an implementation fact needs local diagram context, add a separate Markdown
callout labeled `Implementation observation — observed, not product authority`
with its source, relationship to confirmed intent, and affected IDs. Do not
redraw the canonical target diagram to match an unapproved implementation. If
the product leader adopts an implementer recommendation, leave the observation
as evidence and update the owning target fact and acceptance. Do not change the
observation to `confirmed` or create a decision record unless optional multi-
authority governance genuinely needs one.

## Target baseline

Declare one target baseline in `product.yaml`:

- `greenfield`: no implementation defines the starting product;
- `as_implemented`: reproduce a specifically identified implementation;
- `intended_current`: describe what the product leader intends now; or
- `target_next`: describe a planned future release.

Do not mix baselines inside active intent. A reconstruction can retain observed
facts about several environments while defining only one current target.

## Optional scoped development complexity

Development Complexity Level (DCL) is an optional comparison for one coherent
responsibility in the declared target release. It is not a package score,
maturity framework, acceptance gate, or feature checklist. The owning YAML
record may use this mapping:

```yaml
dcl:
  target:
    level: 3
    status: confirmed
    basis: >-
      Users do not wait for this process, interruption is acceptable, and an
      operator can retry it manually for this release.
  pip_current:
    level: 5
    status: inferred
    basis: >-
      The current PIP requires leasing, automated recovery, and generalized
      orchestration beyond the confirmed target.
  implementation_current:
    level: 4
    status: inferred
    source_ref: git:0123456789abcdef0123456789abcdef01234567
    basis: >-
      The assessed worker retains durable queue recovery but omits some PIP
      mechanisms.
  gap_note: >-
    The PIP appears overbuilt. Simplification may be proposed, while confirmed
    integrity and unsafe-input protections remain required.
```

Apply these semantics:

- Each scope has one owning YAML record or one owning Markdown sequence
  summary. Related artifacts link to it rather than copying the levels or
  basis. Do not add a top-level default, inherit a connected level, or calculate
  a product average or maximum.
- `target.level` is a whole integer from 1 through 10 for this scope and release.
  `target.status` follows normal intent status. A confirmed target is part of
  the canonical PIP. In a package that already uses optional multi-authority
  governance, `decision_id` may identify a decision that owns a disputed or
  delegated target scope. Do not create governance merely for DCL. An agent- or
  implementer-authored target remains `proposed` until adopted into the
  canonical product intent.
- `pip_current` is an `inferred` assessment of sophistication demanded by the
  current PIP logic. `implementation_current` is an `inferred` assessment of
  the implementation and cites its stable snapshot in `source_ref`. Underlying
  mechanisms may be observed; the numeric levels remain inference.
- `gap_note` is required when known values differ. The difference is a review
  signal, not authority to add or remove behavior.
- Omit an unassessed current value rather than inventing one. In the readable
  sequence summary, state `not assessed` or `not implemented` so omission is
  not mistaken for alignment.

Recommend DCL for every sequence that describes an implementable process. Put
a compact target, PIP-current, implementation-current, and gap summary directly
above its Mermaid block. When a YAML record owns the sequence, the summary is a
readable representation of its `dcl` mapping. When Markdown is the only owner,
the summary is sufficient; do not create a sidecar YAML registry solely for
DCL. Do not copy a sequence's DCL into its linked user flow or state machine.

Missing DCL never makes a package incomplete or unready. Existing packages add
it only when a product or implementation review would benefit. Exact confirmed
requirements always override the shorthand level. See
[Development Complexity](development-complexity.md) for the scale, evidence
questions, dangerous-edge rule, mixed-scope example, and interpretation.

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
  Do not create a decision history for a small or single-product-leader team.
  In optional multi-authority governance, retain only decisions whose authority,
  rationale, precedence, or supersession still matters to coordination.

## Engineering discretion

Engineering may choose frameworks, internal modules, algorithms, naming,
repository layout, deployment mechanics, and similar implementation details by
default when the choice does not change confirmed behavior, security, privacy,
data integrity, compatibility, reliability, operability, cost bounds, or other
stated constraints.

Specify or seek authority for a choice only when it crosses that boundary. An
explicit product or technical constraint narrows discretion; a separate
`implementation-discretion.yaml` file is not required.

A confirmed `reuse unchanged` or `modify existing` code anchor and an exact,
authority-confirmed mockup reference are explicit constraints. They are not
unspecified implementation choices. All unmentioned internals remain with
engineering. Companion example or generated design code is reference material
unless separately designated canonical; prefer reuse or adaptation when it is
compatible with the repository and confirmed target.

Routine physical indexes, database-client and pool design, and database
coordination mechanics remain with engineering unless they affect a confirmed
outcome, correctness invariant, performance, quality or cost bound, or
operational capacity. For a product-significant index, use the linked
attribute-badge and `INDEXES`-compartment convention in
[Artifact Responsibilities](artifact-responsibilities.md) and preserve its
intent status. For an explicit application-imposed lock or similar concurrency
restriction, document why the invariant requires it and why a narrower design
cannot preserve the same correctness or capacity outcome while allowing
independent processes to proceed. When aggregate connection fan-out is
product-significant, constrain the relevant deployed process behavior without
inventing a per-process limit or collapsing parallel transactions or
session-bound work that the product needs. Do not present avoidable
serialization, connection amplification, or oversized infrastructure proposed
to compensate for either as an ordinary product requirement.

## Package status

Keep package status in `product.yaml`. Use `draft` or `blocked` until the four
handoff checks pass, then use `status: build_ready`. Do not add a signature,
approval record, confirmation decision, or confirmation revision for a
single-product-leader package. The canonical PIP is the current target and its
Git revision identifies that state. Later observed implementation notes do not
invalidate a clear target. Apply material semantic changes through the team's
normal product-owner and Git workflow; use optional governance only when
several product authorities need explicit coordination. Do not create a
separate readiness ledger. See
[Change and Handoff](change-and-handoff.md).

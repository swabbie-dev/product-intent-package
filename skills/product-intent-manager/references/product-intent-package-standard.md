# Product Intent Package Standard

## Purpose

A Product Intent Package (PIP) is the smallest current description of what
product to build, how people use it, how its consequential processes work, and
which outcomes and constraints matter. It is not a project plan, implementation
log, decision history, or proof that every possible artifact exists.

## Format 7.0

This standard defines format `7.0.0`. Format 7 makes the PIP a pure current-
intent package:

- the default package has three files;
- simple acceptance is inline and a separate acceptance file is conditional;
- package and item statuses, readiness fields, signatures, confirmation
  records, implementation observations, and handoff records are removed;
- alternative intent lives in an isolated PIP fork rather than beside canonical
  intent;
- DCL is an optional product-wide default with narrow overrides; and
- each diagram file succinctly explains the active reasons for its current
  design without recounting product history.

The default package is:

| File | Responsibility |
| --- | --- |
| `product.yaml` | Product name, release, outcome, boundary, actors, capabilities, inline acceptance, exclusions, measures, and optional default DCL |
| `architecture/stack-context.md` | Physical clients, services, managed platforms, stores, external systems, responsibility, owned state, deployment placement, and connections |
| `experience/user-flows.md` | Actor goals, actions, surface topology, visible states, choices, failure, recovery, and outcomes |

Populate these three files. Do not pre-create optional directories or empty
placeholders. Add another artifact only when it communicates distinct
information needed to understand, build, or recognize the intended product.

Use these conventional paths when an optional artifact is needed:

| Optional artifact | Canonical path |
| --- | --- |
| Detailed or cross-capability acceptance | `acceptance.yaml` |
| Multi-authority governance | `governance.yaml` |
| Intended journey | `experience/journeys/JOURNEY-*.md` |
| Screen detail or local mockup | `experience/screens.yaml`, `experience/mockups/` |
| Product-specific design patterns | `experience/design-system.md` or a link to the authoritative design system |
| Rules, state machines, or decision tables | `behavior/rules.yaml`, `behavior/state-machines.md`, `behavior/decision-tables.md` |
| Data model or product-significant schema | `data/data-model.md`, `data/schema.yaml` |
| Shared, external, or product-significant contracts | `contracts/contracts.yaml` or `contracts/openapi.yaml` |
| Runtime sequences | `sequences/sequences.md` |
| Measurable quality constraints | `quality/constraints.yaml` |
| Complex deployment topology | `architecture/deployment.md` |
| Complex coordination topology | `architecture/coordination.md` |

See [Artifact Responsibilities](artifact-responsibilities.md) for the trigger
and ownership of each artifact.

## Canonical current intent

The PIP at the project's canonical location is the current intended product.
Its contents need no `status`, `build_ready`, `confirmed`, `proposed`,
`observed`, `blocked`, or `stale` fields. The package does not contain
signatures, approvals, readiness evidence, implementation observations, review
results, or handoff records. It just describes the current end state.

Keep these outside the canonical PIP:

- discovery evidence and source inventories;
- conversations, questions, alternatives, and product-leader review;
- implementation plans, tickets, assignments, progress, and receipts;
- as-built findings, deviations, audit results, and implementation DCL; and
- superseded requirements and ordinary decision history.

Git records ordinary changes. The task system or concise working notes record
implementation work. Adjacent research, design, operations, schema, or contract
sources remain authoritative for their own detail; link them when needed rather
than copying them into the package.

### Alternative intent uses a PIP fork

When a different end state is being proposed, create an isolated PIP fork in a
branch, worktree, or separate proposal location. The fork must describe one
coherent intended product, not a collection of options or status-labeled
fragments. Its location and review context identify it as noncanonical; do not
add proposal status fields inside it.

Do not place conflicting alternatives in the canonical PIP. Resolve product
questions outside the package. When the product leader adopts the fork, update
the affected canonical intent together through the normal Git process. A direct,
unambiguous product-leader instruction may update canonical intent without a
separate signature or approval record.

## Product record

Keep `product.yaml` flat and readable:

```yaml
schema_version: 7.0.0
name: Example product
release: 1.0.0
outcome: The outcome this release creates for its users.
boundary: What is included in this product and release.

dcl:
  level: 4
  basis: >-
    Users rely on the core path in production, common failures need recovery,
    and current load does not justify generalized scale machinery.

actors:
  - id: ACTOR-001
    name: User
    goal: Complete the primary job.

capabilities:
  - id: CAP-001
    name: Complete the primary job
    actor_ids: [ACTOR-001]
    outcome: The user can recognize that the job completed.
    acceptance:
      - The user can complete the core path and see the resulting state.
      - A common recoverable failure offers a useful next action.

exclusions:
  - A clear consequential exclusion.

success_measures:
  - An observable product measure when one is useful.
```

`outcome` is the user or product result this release creates. `boundary` is the
included and excluded product scope needed to interpret that result. Keep
algorithms, queue behavior, runtime topology, database rules, deployment
settings, retry logic, and similar implementation mechanics in their owning
artifacts. Link those owners when needed instead of repeating their contents in
the root record.

The `dcl` mapping is optional. Omit any other empty field. Add an ID only when
another file or external system references the record. Do not add a package ID
unless something genuinely refers to the package by that ID. Do not duplicate
capability inclusion lists or broad `related_ids` inventories; use direct,
purpose-specific links where a reader needs them.

## Acceptance

Put concise observable acceptance directly on each capability by default. It
should make success and material failure recognizable without dictating
ordinary implementation.

Add `acceptance.yaml` from `assets/acceptance-template.yaml` when acceptance
needs several given/when/then scenarios, spans capabilities, describes material
failure or recovery combinations, or owns detailed measurable quality outcomes.
The separate file then owns those scenarios; do not repeat them inline. It may
link through `verifies` to capabilities, rules, sequences, state transitions, or
quality constraints.

Acceptance is product content, not a readiness gate. It does not require a
package status or a proof report.

## Current rationale

Every diagram file that owns a non-obvious design or architecture choice should
include a concise `Current rationale` section. State all active reasons needed
to understand the current shape, including causal product consequences,
constraints, and material tradeoffs. Prefer wording such as:

- “The API owns the mutation because otherwise the client could become the
  authority for durable state.”
- “These states remain separate because an unknown outcome requires different
  user recovery from a known failure.”

Do not describe when a choice was made, what used to exist, which alternatives
were previously rejected, or the sequence of product changes. Git owns ordinary
history. Remove rationale that no longer explains the current state. Keep a
reason in the diagram file that owns the choice rather than copying it into a
decision log or several diagrams.

## Development Complexity Level

DCL is optional target shorthand, not package status, maturity, acceptance, or
readiness. When used, `product.yaml.dcl` gives the general level and short basis
for the current product. It applies everywhere unless a narrow area materially
differs because of its users, interaction, failure consequence, recovery,
credible load, data sensitivity, security, compliance, or operating needs.

A YAML owner may override it:

```yaml
dcl_override:
  level: 6
  basis: >-
    Interactive retrieval serves a rapidly growing corpus and must remain
    bounded while users wait.
```

A Markdown owner states the same meaning in prose, for example:

```text
**DCL:** 4 (product default)
```

or:

```text
**DCL override:** 6 — Interactive retrieval must remain bounded while users wait.
```

Recommend a DCL line for each implementable sequence. Do not copy an override
onto connected user flows or state machines. Keep implementation assessments
and target-versus-implementation comparisons in audit or task notes outside the
PIP. Exact requirements always override the number. See
[Development Complexity](development-complexity.md).

## Stable IDs and links

Assign a stable ID only when another artifact or external system uses it.
Preserve a cross-file ID through a rename when its meaning is unchanged. Use a
direct purpose-specific field such as `verifies`, `applies_to`, `owned_by`, or a
short prose link. Do not create a central artifact index, traceability graph,
coverage matrix, or duplicate reverse edge merely to show completeness.

Common prefixes include `ACTOR`, `CAP`, `JOURNEY`, `FLOW`, `SCREEN`, `RULE`,
`SM`, `DATA`, `ARCH`, `API`, `EVT`, `SEQ`, `COORD`, `QC`, and `ACC`. A prefix
does not make its artifact type mandatory.

## File formats

- Store structured skill-authored records as YAML in `.yaml` files.
- Use unique string keys. Avoid YAML aliases, anchors, and custom tags.
- Store Mermaid source in Markdown `.md` with a fenced `mermaid` block, even
  when the file contains only a diagram.
- Do not create canonical skill-authored `.json` or `.mmd` files.
- Keep external contracts or evidence in a required source format when needed
  and link to them instead of converting them for cosmetic consistency.
- Track the package in Git.

## Engineering discretion and implementation anchors

Engineering may choose frameworks, internal modules, algorithms, naming,
repository layout, and similar internals when the choice does not change the
PIP's behavior, security, privacy, data integrity, compatibility, reliability,
operability, cost bounds, or other stated constraints.

When implementation reuse matters, a sequence should name the verified path and
symbol and say `reuse unchanged` or `modify existing`. Name `new` code only when
no suitable owner exists or the PIP requires a separate responsibility. For
each consequential sequence input, state its source: user and surface, named
function parameter or return, persisted field, external payload, or named
constant, configuration, or setting.

An exact mockup linked as the current release target is binding visible and
interaction intent. Implementers must preserve its surfaces, components,
content hierarchy, states, and interactions and should adapt compatible example
or export code when available. They must not silently add, remove, merge, split,
or redesign the target. Generated code is implementation reference, not an
exception to repository, accessibility, security, or product constraints.
A whole design-file, project, board, or folder link supplies context but is not
an exact target; identify the governing frame, node, branch, version, or local
mockup next to the affected surface.

Routine indexes, connection-pool design, and database coordination remain with
engineering unless they affect a stated product outcome, invariant, quality or
cost bound, or operational capacity. Product-significant indexes use the ERD
badge plus `INDEXES` compartment convention. Explicit application-controlled
locks and broad serialization require a named invariant and the narrowest
mechanism that protects it while preserving independent work. Connection design
should consolidate clients or pools within a process when that reduces fan-out
without harming necessary concurrency or session behavior. See
[Artifact Responsibilities](artifact-responsibilities.md).

An ERD is selective but exact about persisted product behavior. Show each
persisted column individually with its physical name, type, and material
constraint when it affects selection, ranking, eligibility, authorization,
lifecycle, recovery, compatibility, visible outcomes, or product-significant
audit behavior. Omit incidental implementation columns, and clearly label an
abbreviated entity repeated only as a cross-diagram reference projection. Never
collapse product-significant columns into a synthetic grouped field. Every
index or coordination badge requires the exact physical column and type.

## Optional governance

Do not create `governance.yaml` for a small team or a product whose decisions
route through one product leader. Team size, implementation contributors, and
specialist review roles do not by themselves justify it.

Use optional governance only when several product leaders or delegated
authorities need durable scope, precedence, or supersession context to avoid
cross-team conflict. Keep only that coordination information. Do not put current
requirements, design rationale, open proposals, implementation observations,
readiness, signatures, or routine history there. The owning PIP artifact remains
the current doctrine; Git remains ordinary history.

## Tasks and checks stay outside the PIP

The existing task system or working notes own the minimal steps, assignments,
dependencies, progress, and implementation verification needed to reach the
PIP. They do not become product authority and must not be mirrored into the
package.

The skill's coherence, format, and implementation-alignment checks describe how
an agent should use the PIP. They do not create PIP files, fields, gates,
signatures, readiness labels, or handoff reports. See
[PIP Use and Alignment Checks](change-and-handoff.md).

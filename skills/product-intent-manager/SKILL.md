---
name: product-intent-manager
description: Create, reconstruct, simplify, or update an explicitly requested Product Intent Package (PIP), or preserve its current intent while planning, implementing, or auditing work governed by it. Use when the user asks to work on a PIP or explicitly implement or audit against one; do not activate for ordinary product planning, diagramming, coding, or project documentation with no PIP.
---

# Product Intent Manager

## Read this first: diagram responsibilities

Keep these boundaries clear from the start:

- **Sequence diagrams hold detailed process logic:** ordered calls and events,
  input sources, existing code to reuse or modify, decisions, durable changes,
  retries, fallbacks, timeouts, partial failures, and recovery.
- **State machines show high-level process interaction:** stable lifecycle states
  and the transitions produced by the processes represented in sequence
  diagrams. They intentionally omit each process's internal logic.
- **User flows show the user experience and mockup inventory:** actor actions,
  clearly bounded user-visible surfaces and states, navigation, visible failure
  and recovery, and outcomes. They intentionally omit internal system logic.

Missing sequence-level detail in a state machine or user flow is correct. Link
to the owning sequence instead of copying its internals into those views.

## The canonical PIP is current intent

The canonical PIP is the product's current intended end state. It does not need
status fields, readiness labels, signatures, confirmation records, handoff
records, implementation observations, or proposal markers. It simply states
what the product is meant to be. Git records ordinary history.

Keep conversations, evidence, unresolved questions, implementation findings,
tasks, and review results outside the canonical package. If someone wants to
propose a different end state, create an isolated PIP fork in a branch,
worktree, or separate proposal location. Make that fork internally coherent as
one complete intended end state; do not mix competing alternatives into the
canonical package. Its location makes it noncanonical, so its records need no
`proposed` status. Adopt it by replacing the affected canonical intent through
the team's normal product-leader and Git process.

For a small team or a product routed through one product leader, do not create
`governance.yaml`, authority registries, decision histories, signatures, or
approval metadata. Optional governance is only for a larger team in which
several product leaders or delegated authorities need explicit scope,
precedence, or supersession to coordinate decisions. It must not duplicate the
current requirements or rationale owned by the product artifacts.

## Keep the package proportional

The default package has three files:

```text
product.yaml
architecture/stack-context.md
experience/user-flows.md
```

Put simple observable acceptance directly on the capability in `product.yaml`.
Add `acceptance.yaml` only when several scenarios, failure paths, cross-
capability behavior, or detailed quality outcomes would make inline acceptance
hard to read. Add any other artifact only when it answers a distinct product
question. Read the
[Package Standard](references/product-intent-package-standard.md) before
creating or migrating package structure and
[Artifact Responsibilities](references/artifact-responsibilities.md) before
choosing or separating diagrams.

Use one owner for each fact and direct links where another artifact needs
context. Assign a stable ID only when another file or external system refers to
the item. Do not create artifact indexes, traceability graphs, coverage
matrices, change logs, readiness ledgers, or placeholder files.

## Explain the current design, not its history

In the diagram file that owns a design or architecture choice, add a short
`Current rationale` section. State every active reason needed to understand why
the current design is shaped that way, using causal language such as “X is
necessary because otherwise Y can occur.” Include product consequences,
constraints, and material tradeoffs; keep it concise.

Describe the reasons for the current state, not the chronology of how it was
reached. Do not recount former designs, superseded decisions, dates, or a series
of changes. Remove a reason when it no longer explains the current design. Git
owns ordinary history; exceptional multi-authority coordination belongs only in
optional governance.

## Development Complexity Level

Development Complexity Level (DCL) is an optional shorthand for the general
engineering and operational stage the current product intent requires. When it
is useful, put one product-wide default in `product.yaml`:

```yaml
dcl:
  level: 4
  basis: >-
    Users depend on this path in production, common failures need automatic
    recovery, and current load does not justify generalized scale machinery.
```

The default applies everywhere unless a narrowly defined area has materially
different user needs, failure consequences, load, security, compliance, or
operational demands. Give that owner a `dcl_override` with its own `level` and
`basis`. Recommend a visible DCL line above each implementable sequence, either
`DCL: 4 (product default)` or `DCL override: 6 — <current reason>`.

DCL describes target intent only. Keep implementation DCL assessments and
target-versus-implementation comparisons in audit or task notes outside the
PIP. It is not a readiness score, acceptance gate, or reason to add machinery.
Use the lowest level that safely fits actual users, interactions, recovery,
risk, and credible load. A low DCL never weakens authorization, security,
privacy, money safety, data integrity, or destructive-operation protections.
Read [Development Complexity](references/development-complexity.md) before
assigning or changing a level.

## Prevent implementation drift

When the PIP governs implementation or an implementation-oriented sequence:

- **Reuse before adding.** Inspect the code and name the existing function,
  handler, job, or module that should be `reuse unchanged` or `modify existing`.
  Specify `new` only after confirming there is no suitable owner or a stated
  constraint requires separation.
- **Name input provenance.** For each input that affects a branch, durable
  change, visible outcome, or acceptance, state whether it comes from a user
  and surface, a named function parameter or return, a persisted field, an
  external payload, or a named constant, configuration, or setting.
- **Follow exact mockups.** A mockup linked as the current release target is the
  required surface, component, state, content hierarchy, and interaction
  design. Use compatible example or exported code when available. Do not add,
  remove, merge, split, or materially redesign views or components without the
  product or design leader changing the target. Raise feasibility,
  accessibility, security, or repository conflicts instead of silently
  deviating.

Engineering owns unspecified internals when they do not change current
behavior, security, privacy, data integrity, compatibility, reliability,
operability, cost bounds, or other stated constraints.

## Data access and concurrency

Record database mechanics only when they are product-significant:

- For a consequential index, show a textual, color-matched badge on every
  affected ERD attribute and repeat the badge in an `INDEXES` compartment below
  the entity. The compartment owns the current definition and the product or
  process reason. Omit routine implementation indexes.
- Before allowing several database clients or pools in one process, check
  whether a bounded shared pool can combine them without serializing genuinely
  independent transactions, causing head-of-line blocking, breaking session
  semantics, or reducing effective product performance. Consider total fan-out
  across replicas, workers, and overlapping jobs; do not invent numeric limits.
- Treat application-controlled locks, stronger-than-normal isolation,
  singletons, and similar restrictions on otherwise independent work as
  exceptional. Use one only for a named correctness invariant or material
  capacity bound that a narrower constraint, atomic statement, optimistic
  check, idempotency rule, short transaction, or partitioned design cannot
  protect. Do not require oversized database infrastructure to compensate for
  avoidable contention.

See [Artifact Responsibilities](references/artifact-responsibilities.md) for
the diagram conventions.

## Minimal implementation tasks

The PIP owns the end state. The existing task tracker or concise working notes
own only the smallest practical steps to reach it. Keep tasks outside the PIP
and link them to the relevant PIP records instead of restating the package.

A task needs only the intended outcome, a relevant PIP link, a verified code or
design anchor when it prevents guesswork, an observable done condition, and the
smallest useful verification. Split only for independent ownership, dependency
order, material risk, or separately shippable scope. Do not create a ticket per
file, layer, diagram, scenario, or implementation step.

For each task, ask whether every instruction directly aligns the codebase with
the PIP, whether it can be removed or merged, whether existing code and tests
can be reused, and whether each requested test, gate, proof, or review protects
a core outcome or dangerous edge case. Verify the core path, PIP-required
failure or recovery behavior, and dangerous edge cases; do not demand exhaustive
permutations, blanket coverage, new test machinery, or proof artifacts.

## Workflow

1. Read the canonical package, repository guidance, and the relevant references
   below. For a new package, copy `assets/product-intent-template/`.
2. Establish the release, outcome, boundary, actors, capabilities, exclusions,
   measures, and optional product-wide DCL.
3. Put simple acceptance on each capability; add the optional acceptance file
   only when scenario detail needs its own owner.
4. Draft the physical stack context and user-visible flows. Add state, data,
   sequence, rule, contract, journey, screen, quality, or deployment detail only
   when it resolves a real ambiguity.
5. Add concise current rationale to each owning diagram file. Link related
   records directly instead of copying their content.
6. Use an isolated PIP fork for an unadopted alternative. Keep reconstruction
   evidence, questions, and implementation comparison outside the package.
7. Apply the lightweight checks in
   [PIP Use and Alignment Checks](references/change-and-handoff.md). Those
   checks govern how people use the PIP; they never create fields, files, gates,
   signatures, or reports inside the PIP.

For create, reconstruct, update, implementation-audit, and simplification
details, read [Workflows](references/workflows.md). For evidence and product-
authority boundaries, read
[Authority and Evidence](references/authority-and-evidence.md).

## Rules

- Use YAML in `.yaml` files for structured records.
- Store Mermaid in fenced `mermaid` blocks in Markdown `.md` files, including
  files that contain only a diagram. Do not create skill-authored canonical
  JSON or `.mmd` files.
- Keep the canonical PIP free of status, readiness, proposal, implementation,
  handoff, and review metadata.
- Track the package in Git. Use Git history instead of duplicating change
  history inside the PIP.
- Keep task state and implementation notes outside the package.
- Check changed YAML, direct links, Mermaid output, and whitespace in
  proportion to the change. Do not add a validator, package hash, snapshot
  suite, or readiness gate for ordinary documentation work.
- This skill does not itself authorize product implementation, external writes,
  task mutations, commits, or pushes.

## Deliver

Return the requested PIP update or implementation-alignment result with a short
summary of the current release boundary, material package changes, optional
artifacts added or removed, and any product question that remains outside the
canonical PIP. When implementation was requested, report material deviations
and the minimal task or verification scope separately from the PIP.

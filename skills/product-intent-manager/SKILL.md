---
name: product-intent-manager
description: Create, reconstruct, simplify, or update an explicitly requested Product Intent Package (PIP), or preserve its current intent while planning, implementing, or auditing work governed by it. Use when the user asks to work on a PIP or explicitly implement or audit against one; do not activate for ordinary product planning, diagramming, coding, or project documentation with no PIP.
---

# Product Intent Manager

## Read this first: diagram responsibilities

Keep these boundaries clear from the start:

- **Sequence diagrams hold detailed process logic:** ordered calls and events,
  input sources, intended code ownership, decisions, durable changes,
  retries, fallbacks, timeouts, partial failures, recovery, polling, heartbeats,
  lease renewal, and the tables and access paths used by consequential database
  steps.
- **State machines show high-level process interaction:** stable lifecycle states
  and the transitions produced by the processes represented in sequence
  diagrams. They intentionally omit each process's internal logic and routine
  self-loops that do not change a stable lifecycle state.
- **User flows show the user experience and mockup inventory:** actor actions,
  clearly bounded user-visible surfaces and states, navigation, visible failure
  and recovery, and outcomes. They intentionally omit internal system logic. A
  binding design target identifies the exact frame, node, branch, version, or
  local mockup; a link to an entire design file is context only.

Missing sequence-level detail in a state machine or user flow is correct. Link
to the owning sequence instead of copying its internals into those views.

## The canonical PIP is current intent

The canonical PIP is the product's current intended end state. It does not need
status fields, readiness labels, signatures, confirmation records, handoff
records, implementation observations, or proposal markers. It simply states
what the product is meant to be. Git records ordinary history.

Write every PIP artifact as present-tense product facts or timeless requirements:
“The sign-in surface uses the provider's native component” or “Use the provider's
native component for sign-in.” Describe the intended result, not how to reach
it or what it replaces. Never put reuse/modify directions, “replace the old,”
“will add,” migration steps, or completed-work narration in the PIP; those
belong only in external tasks or notes.
This applies to diagram labels, supporting notes, and acceptance too. Detailed
runtime logic and required components or code owners still belong in the PIP;
construction instructions do not. Present-tense intent is not a claim that the
implementation already matches it.

Keep conversations, evidence, unresolved questions, implementation findings,
tasks, and review results outside the canonical package. If someone wants to
propose a different end state, create an isolated PIP fork in a branch,
worktree, or separate proposal location. Make that fork internally coherent as
one complete intended end state; do not mix competing alternatives into the
canonical package. Its location makes it noncanonical, so its records need no
`proposed` status. Adopt it by replacing the affected canonical intent through
the team's normal authorized-editor and Git process.

Add `governance.yaml` when agents or contributors need a durable way to confirm
who may request canonical PIP edits. It records current editing authority only:
at least one product leader with `full` access, plus any `scoped` or
`proposal_only` contributors. It contains no decisions, approvals, signoffs,
change records, requirements, rationale, or history; Git records who committed
each change. A `scoped` editor may not leave canonical intent partial or
contradictory. If a coherent change needs dependent edits outside that scope, a
`full` editor must make the complete change or the work stays in an isolated
PIP fork. Read [Authority and Evidence](references/authority-and-evidence.md)
before accepting or applying a canonical edit request.

Use the team's existing task manager or implementation notes alongside the PIP.
The PIP does not define task management, a ticket format, or a delivery workflow.
Tickets in Linear, Notion, ClickUp, GitHub, or another task system are execution
overlays, not secondary product specifications. A ticket may narrow what an
implementation pass will touch, but it must point to the
canonical PIP for product behavior, acceptance, constraints, diagrams, and
design targets rather than paraphrasing them. If a ticket conflicts with its
linked PIP, the PIP governs and the ticket must be corrected or clarified.

Audit against the canonical PIP, not against a ticket's wording. A ticket may
identify which implementation area and PIP records to inspect, but the linked
PIP supplies the expected behavior, acceptance, constraints, and design. Ticket
status, checklists, tests, or paraphrased requirements do not prove PIP
alignment. Report ticket drift separately from implementation drift.

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

Keep the root product record outward-facing. `outcome` states the user or
product result. `boundary` states what this product and release include and
exclude. Do not turn either into an inventory of algorithms, queues, database
mechanics, deployment settings, or concurrency rules; put those facts in their
owning artifacts and link them when context is necessary.

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
owns ordinary history; optional governance records only current editing
authority.

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

DCL never requires automatic handling of every edge case. When the PIP does not
already resolve a rare or complex case, ask the product manager, originator, or
other human product authority before designing, implementing, or extensively
testing it. Clarify whether current intent is automatic handling, manual review
or recovery, visible failure or deferral, or exclusion from the release. Do
this at every DCL; a high DCL does not make costly rare-case automation
automatically worthwhile. Record the chosen behavior in the owning PIP artifact
before implementation. A manual path must still contain the case safely until
review; it cannot defer an authorization, security, privacy, money,
data-integrity, or destructive effect until after harm occurs.

For an intentional manual fallback, prioritize reliable admin awareness over a
complete admin control surface. The owning PIP behavior should require the
responsible admin or operator to be notified with enough context to identify the
incident, understand its safe current state, and find the existing place or
procedure for investigation. When a sequence exists, show that notification or
handoff. Use an existing monitored channel when it is sufficient; a passive log
no one is expected to watch is not visibility. Do not invent dashboards,
queues, retry buttons, editors, overrides, or other controls for every possible
fallback. Add a dedicated control only when the chosen manual procedure
actually requires that action and existing tools are insufficient, or when
frequency, urgency, or volume justifies it.

Read [Development Complexity](references/development-complexity.md) before
assigning or changing a level.

## Prevent implementation drift

When the PIP governs implementation or an implementation-oriented sequence:

- **Name intended code ownership.** Inspect existing code and identify the
  function, handler, job, or module that owns the process, for example
  “`path::function` handles this request.” Preserve suitable existing owners
  instead of creating parallel implementations. Keep whether to reuse, modify,
  or add code in external implementation notes, not PIP action labels.
- **Name input provenance.** For each input that affects a branch, durable
  change, visible outcome, or acceptance, state whether it comes from a user
  and surface, a named function parameter or return, a persisted field, an
  external payload, or a named constant, configuration, or setting.
- **Follow exact mockups.** A mockup linked as the current release target is the
  required surface, component, state, content hierarchy, and interaction
  design. A whole design-project or file link is useful context but is not an
  exact implementation target; identify the governing frame, node, branch,
  version, or local mockup next to the affected surface. Use compatible example
  or exported code when available. Do not add, remove, merge, split, or
  materially redesign views or components without the product or design leader
  changing the target. Raise feasibility, accessibility, security, or
  repository conflicts instead of silently deviating.

Engineering owns unspecified internals when they do not change current
behavior, security, privacy, data integrity, compatibility, reliability,
operability, cost bounds, or other stated constraints.

For an audit, use tickets only to locate the requested scope, affected code,
and implementation evidence. Reopen the canonical PIP release or revision and
derive every product-alignment criterion from its owning records. Follow direct
links and obvious semantic dependents needed to judge that scope; do not turn
ticket acceptance or completion status into the audit target.

## Data access and concurrency

Record database mechanics only when they are product-significant:

- An ERD may omit incidental implementation columns, but it must show each
  persisted column that directly determines product behavior as its own row
  with the exact physical name, type, and product-significant constraint. This
  includes facts that affect selection, ranking, eligibility, authorization,
  lifecycle, recovery, compatibility, visible outcomes, or product-significant
  audit behavior. Do not hide them in a synthetic row such as
  `fitness_controls SMALLINT × 5`. A clearly labeled cross-diagram reference
  projection may stay abbreviated and link to the owning `DATA-*` entity.
- In each consequential database step in a sequence, name the operation,
  `DATA-*` ID, and exact physical table or view. Default to the owning ERD's
  index badge when that index is the intended access path; otherwise list the
  key lookup, join, filter, or mutation fields. When one logical step uses
  several tables, name each table and its read, join, write, or constraint role.
  Keep the database service as the lifeline, link rather than repeat the ERD's
  full index definition, and do not claim the database planner is guaranteed to
  choose an index unless that guarantee actually exists.
- For a consequential index, show a textual, color-matched badge on every
  affected ERD attribute and repeat the badge in an `INDEXES` compartment below
  the entity. One base badge such as `[I1]` identifies exactly one complete
  physical index definition; never group two indexes under one badge, even when
  their keys or purpose overlap. Give indexes with different predicates,
  expressions, included columns, uniqueness, methods, directions, or key order
  separate badges. For one index, use a numeric suffix for a direct ordered key,
  `·expr` for a separate indexed expression, `·inc` for an included column, and
  `·where` only for a predicate-only column. Do not add `·where` to a column
  already represented as that index's direct key or expression. The compartment
  owns each full definition and its product or process reason. Keep an ordinary
  primary key as `PK` in the entity and omit its index badge unless the physical
  index has an independently product-significant purpose. Omit routine
  implementation indexes. Every index or coordination badge must sit on the
  exact physical column it describes, never on a grouped or synthetic row.
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
- When several processes or coordination mechanisms make contention hard to
  understand, add a coordination overlay to `architecture/stack-context.md`.
  It shows the contenders, narrow scope, mechanism, storage or owner, expiry or
  fencing when applicable, and protected resource. Keep one straightforward
  lock or lease in its sequence and, for persisted lease fields, its ERD. Split
  the overlay into `architecture/coordination.md` only when stack context would
  otherwise become unreadable.

See [Artifact Responsibilities](references/artifact-responsibilities.md) for
the diagram conventions.

## Boundary with companion implementation tasks

The PIP owns the end state. Companion tickets or working notes own the smallest
practical execution context needed to reach it, including reuse/modify
directions. The following guidance keeps those notes subordinate to the PIP;
it does not prescribe a task-management process. Identify the canonical PIP
release or revision and link directly to the relevant record
IDs or files. Do not copy, summarize, reinterpret, or rewrite the PIP's product
behavior, acceptance, constraints, sequence logic, data rules, or mockup
requirements into the ticket; parallel wording can be mistaken for authority
and drift from its owner.

A useful ticket contains implementation-specific information: the execution
boundary—including what to touch and what not to touch—verified code or design
anchors, essential order, codebase-specific tips and hazards, blockers,
assignment or progress, and proportional verification evidence.

Use a concise implementation objective or PIP IDs for the ticket title. Define
completion as alignment with the linked PIP plus task-specific evidence; do not
duplicate PIP acceptance as a ticket checklist. If the PIP lacks required
product meaning, resolve or update the PIP through its authority process rather
than filling the gap in a ticket. Split only for independent ownership,
dependency order, material risk, or separately shippable scope. Do not create a
ticket per file, layer, diagram, scenario, or implementation step. Read
[PIP Use and Alignment Checks](references/change-and-handoff.md#minimal-implementation-tasks)
when creating or reviewing implementation tasks.

For each task, ask whether every instruction directly aligns the codebase with
the PIP, whether it can be removed or merged, whether existing code and tests
can be reused, and whether each requested test, gate, proof, or review protects
a core outcome or dangerous edge case. Verify the core path, PIP-required
failure or recovery behavior, and dangerous edge cases; do not demand exhaustive
permutations, blanket coverage, new test machinery, or proof artifacts.
Before expanding a task around a rare or complex edge case the PIP does not
resolve, confirm the intended automatic, manual, visible fallback, or excluded
behavior with a human product authority rather than inferring it from DCL.

## Workflow

1. Read the canonical package, `governance.yaml` or the repository's current
   editing-authority guidance, and the relevant references below. Confirm that
   the requester has authority for the complete coherent change. For a new
   package, copy `assets/product-intent-template/`.
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
  handoff, review, signoff, and decision-history metadata. Optional
  `governance.yaml` contains current editing authority only.
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

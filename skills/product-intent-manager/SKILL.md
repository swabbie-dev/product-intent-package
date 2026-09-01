---
name: product-intent-manager
description: Create, reconstruct, simplify, or update an explicitly requested Product Intent Package (PIP), or preserve its current target while planning, implementing, or auditing work governed by it. Use when the user asks to work on a PIP or explicitly implement or audit against one; do not activate for ordinary product planning, diagramming, coding, or project documentation with no PIP.
---

# Product Intent Manager

Maintain the smallest package that communicates what product to build, why it
matters, how people use it, and which observable outcomes constrain
implementation. Do not turn the package into an implementation specification
or a proof that every possible document exists.

## Canonical PIP and implementation evidence

For a small team or a product routed through one product leader, the canonical
PIP is the current product intent. Git records how it changed. Do not create
`governance.yaml`, authority registries, decision histories, signatures,
approval references, or confirmation revisions for these teams.

Use optional governance only for a larger team in which several product leaders
or delegated authorities can make overlapping decisions and readers need
explicit scope, precedence, supersession, or durable cross-team rationale. Even
then, a governance decision never repeats product content; diagrams, rules,
requirements, and acceptance remain the doctrine owners.

Team size, implementation contributors, or specialist reviewers alone do not
justify governance. If product-intent choices still route through one product
leader, omit it.

Use these meanings consistently when content is not simply current target intent:

- `confirmed`: current target doctrine in the canonical PIP;
- `observed`: current implementation evidence, never product authority;
- `proposed`: a candidate target change not yet adopted into the canonical PIP;
  and
- `blocked` or `stale`: content that must not govern implementation yet.

Do not add an `authorization_level`, signature, or confirmation field. Record a
material as-built difference separately as an implementation observation. Keep
ordinary changes and history in Git.

When creating, changing, implementing, or auditing work governed by a PIP:

- **Preserve the target baseline.** Identify the task-start canonical PIP Git
  revision and any later direct product-leader instructions in the existing
  task or working context. Do not create another ledger. New semantic claims do
  not become target intent merely because an implementer edits a working copy.
- **Prevent circular adoption.** New or changed semantic claims introduced
  in PIP edits, tickets, tests, audit findings, diagrams, or implementation
  receipts during the same work remain `observed` or `proposed` unless the
  product leader adopts them. These artifacts cannot validate one another as
  product intent. Permission to implement, migrate, commit, or push does not by
  itself adopt a new product meaning.
- **Separate doctrine from implementation evidence.** Keep confirmed target
  facts in their owning artifacts. Put a material current implementation fact
  beside its owner as a visibly separate local YAML record or Markdown callout
  labeled `Implementation observation — observed, not product authority`. A
  multi-authority package that already needs governance may instead use its
  sparse `implementation_observations` list for a cross-artifact fact. Every
  observation stays `observed`, cites a `source_ref`, links affected IDs when
  useful, and says whether it `aligns`, `deviates`, or is `unclear` relative to
  current intent. Routine and superseded history stays in Git or the task
  system. The optional scoped
  `dcl.implementation_current` assessment below may keep only a rough inferred
  level, stable source reference, and concise basis beside its target; it does
  not replace the observation lane or make implementation evidence doctrine.
- **Do not normalize divergence into doctrine.** When implementation differs
  from the current target, preserve the target and record the implementation as
  observed. Keep an implementer recommendation visibly `proposed` in the owning
  artifact or existing task system. Use `governance.yaml.open_items` only when
  optional multi-authority governance already exists and the authorities must
  coordinate the proposal. If the product leader adopts it, update the owning
  target facts and acceptance through the normal Git workflow; never change the
  observation itself to `confirmed`.

## Semantic expansion boundary

A constraint at one processing boundary does not authorize moving it to
another. For example, `safe to expose` does not mean `eligible to retrieve`
unless the current PIP or product leader establishes that relationship. Qualify
ambiguous terms such as `eligible`, `safe`, `valid`, and `shared` with the domain, stage,
population, data, algorithm, lifecycle, or output they actually constrain.

Pause for one concise authority question before an implementation mechanism
absent from confirmed intent would:

- create a durable eligibility, admission, exclusion, or classification;
- split a population, corpus, audience, or product surface;
- move a rule between authorization, retrieval, ranking, projection,
  publication, or persistence;
- add maintained derived state or a broad existing-data backfill;
- encode product policy in a constraint or partial-index predicate; or
- materially change privacy, membership, operating cost, or system load.

State the product effect, persistence or migration effect, and smallest viable
alternative. Do not add an approval ceremony for ordinary engineering choices
that remain inside confirmed outcomes and constraints.

## Scoped development complexity

Use Development Complexity Level (DCL) only as an optional, scoped comparison
between the engineering sophistication justified by confirmed product needs,
the sophistication currently encoded by the PIP, and the sophistication found
in an assessed implementation. Read
[Development Complexity](references/development-complexity.md) before assigning
or changing a level.

Determine DCL only after understanding the current target release, actors, user
interactions, whether users wait for the process, failure consequences, manual
operation and recovery, real and credible near-term load, data sensitivity,
security or compliance constraints, and operating cost. Assign it to the
smallest coherent responsibility or process. Different parts of one product
may legitimately require very different levels. Never create, inherit, average,
or enforce one package-wide DCL. Give each scope one owner and link related
artifacts instead of copying its values.

An optional `dcl` mapping may appear on a YAML record when the comparison helps
readers make or review implementation decisions. Recommend it for each
implementable `SEQ-*` process. A sequence stored in Markdown shows a compact
DCL summary immediately above the Mermaid diagram so the values are visible
with the logic; when a YAML record owns the sequence, the summary represents
that record rather than creating another authority source. Keep these meanings
separate:

- `target` is proposed or current product doctrine for the declared release;
  when optional multi-authority governance already exists, a specific `DEC-*`
  may own a disputed or delegated scope;
- `pip_current` is an `inferred` assessment of the complexity demanded by the
  current PIP logic; and
- `implementation_current` is an `inferred`, source-referenced assessment of
  the implementation as of an identified revision.

When known values differ, add a concise `gap_note` explaining whether the
difference is intentional, an open PIP deficiency, incomplete implementation,
or possible overbuilding. A DCL difference is a review signal, not authority to
delete or add machinery. Exact confirmed requirements override the shorthand
level. A low DCL never waives authorization, security, privacy, data-integrity,
money-safety, destructive-operation, or similarly dangerous-edge protections.
Diagram size and detail do not determine DCL.

## Diagram detail boundary

Sequence diagrams own detailed process logic. State machines and user flows
intentionally omit that detail because they answer different questions:

- **Sequence diagram — detailed process logic.** Show how one consequential
  process executes: participating systems, ordered calls or events, material
  decision branches, retries, fallbacks, timeouts, partial failures,
  compensation or recovery, and durable state changes.
- **State machine — high-level process interaction.** Show stable lifecycle
  states and how the processes represented by sequences move the subject
  between those states. Label or link each consequential transition to its
  `SEQ-*` when available. Do not copy process steps, message order, retry or
  fallback branches, or other sequence internals into the state machine.
- **User flow — visible experience and mockup inventory.** Show actor actions,
  user-visible surfaces and states, navigation, visible failure and recovery,
  and terminal outcomes. Bound each consequential surface so designers can see
  which pages, views, dialogs, panels, or messages need mockups. Do not show
  API, database, service, or other internal process logic.

Missing internal process logic in a state machine or user flow is correct, not
a documentation gap. A state machine shows how processes connect through
lifecycle transitions; it is not another process-flow diagram. Never add
sequence-level detail merely to make a state machine or user flow appear
complete. Link to the owning sequence instead.

## Implementation anchors and confirmed design

Do not leave the following matters to implementation guesswork when they apply:

- **Reuse before adding.** Inspect the relevant code. In each sequence, name
  only the existing functions, handlers, or modules needed to prevent duplicate
  work. Give the verified path and symbol in the message or an adjacent note and
  label it `reuse unchanged` or `modify existing`. Do not call for a parallel or
  replacement function unless no suitable owner exists or a confirmed technical
  decision requires one.
- **Name input provenance.** For every consequential sequence input, state its
  source inline or in a note: user input and surface, parameter or return from a
  named function, persisted field, external payload or event, or named constant,
  configuration, or setting. Include inputs that affect a branch, durable
  change, visible outcome, or acceptance; omit incidental local variables.
- **Implement confirmed mockups.** Link the exact frame or node, version, intent
  status, and any companion example or export code. An authority-confirmed,
  in-scope mockup is the required visible and interaction target, not inspiration
  or documentation-only. Prefer reuse or adaptation of its companion code when
  compatible with the repository. Do not add, remove, merge, split, or materially
  alter its views, components, or states without accountable product or design
  approval. Raise feasibility, accessibility, security, or compatibility
  conflicts instead of silently deviating. Generated or exported code is a
  reference unless it is separately designated canonical.

## Data access and concurrency

When database access or coordination can affect a confirmed product outcome,
cost bound, or operational constraint, read
[Artifact Responsibilities](references/artifact-responsibilities.md):

- **Show consequential indexes in context.** In a table-style ERD, place a
  textual, color-matched index badge on every affected attribute row and repeat
  that badge in an `INDEXES` compartment below the entity. The compartment owns
  the confirmed definition or proposed index intent, status, and product or
  process purpose. Color supplements the badge text; it never replaces it. Omit
  routine indexes that do not constrain product intent. An index may support a
  confirmed product rule; its predicate cannot establish that rule.
- **Bound connection fan-out.** When connection use can affect confirmed
  performance, reliability, capacity, or cost, first check whether work within
  each process can reuse a bounded shared pool or consolidate database clients
  without serializing independent transactions, causing head-of-line blocking,
  or reducing effective product performance. Assess aggregate fan-out across
  process pools, replicas, workers, overlapping jobs, and dedicated sessions.
  Preserve distinct connections or pools for genuinely concurrent transactions,
  session-bound listeners, streams or long-running work, and workload isolation
  when needed. Do not invent a numeric cap or benchmark requirement without a
  confirmed provider limit or product constraint.
- **Preserve useful concurrency.** Treat explicit application-imposed database
  locks, stronger-than-default isolation that materially restricts concurrency,
  singleton requirements that block otherwise independent work, and similar
  serialization as exceptional. Use one only when a named correctness invariant
  or material capacity bound cannot be protected by a simpler, narrower
  mechanism that still permits independent work. Record the invariant and only
  the scope, duration, affected processes, timeout, recovery, capacity cost, and
  rejected alternatives material to that outcome or bound. Do not require
  oversized database infrastructure merely to compensate for avoidable
  contention. This rule does not prohibit the database's ordinary short-lived
  internal locks while executing atomic statements or enforcing constraints.

## Minimal implementation tasks

The PIP owns the desired end-state. The project's existing task tracker or
implementation notes own only the smallest steps needed to move the current
product to that end-state. Keep those tasks outside the PIP and link them to the
target release and relevant PIP IDs instead of restating the package. PIP work
does not itself authorize creating or changing tickets in an external system;
draft them unless that write is already authorized.

When implementation planning is requested, derive the smallest coherent task
set from confirmed PIP intent. A task needs only the intended outcome, relevant
PIP links, a verified code or design anchor when it prevents guesswork, an
observable done condition, and the smallest useful verification. Split work
only when independent ownership, dependency order, material risk, or release
scope makes the split useful. Do not create a ticket per file, layer, diagram,
acceptance scenario, or implementation step.

Before retaining a task or instruction, ask:

- Does it directly help align the codebase with the confirmed PIP end-state?
- Is it more detailed than the implementer needs, or can it be removed or
  merged?
- Does it reuse the existing code, tests, tools, and project process where
  practical?
- Does every requested test, gate, proof, report, or review protect a core
  product outcome or a dangerous edge case?

Remove ceremony that fails those questions. Verification should cover the core
path, material failure or recovery behavior named by the PIP, and dangerous
edge cases relevant to the change. Dangerous means a plausible failure could
cause an authorization, security, or privacy breach; a money error; data loss
or corruption; an unsafe schema or migration result; a destructive or
irreversible side effect; or another comparably high-impact product or
operational harm. Do not demand exhaustive permutations, blanket coverage
targets, new test machinery, proof documents, or readiness gates.

## Choose the work mode

- **Create:** define a new product or release from an idea.
- **Reconstruct:** distinguish observed product behavior from intended behavior.
- **Complete:** close material gaps in an existing package.
- **Update:** change confirmed intent and its affected dependents.
- **Simplify:** remove duplicate machinery without losing product meaning.
- **Implement or audit:** preserve the current target while comparing planned
  or observed implementation against its task-start PIP revision.

## Workflow

1. Read the existing package and repository guidance. For a new package, start
   from the four-file template in `assets/product-intent-template/`.
2. Establish the target baseline and release boundary, desired outcome, actors,
   capabilities, exclusions, measures, and the product leader or normal project
   route that maintains the canonical PIP. Do not record that route inside a
   small-team PIP.
3. Add an artifact only when it resolves a real product, experience, behavior,
   data, system, quality, or acceptance question. Read
   [Artifact Responsibilities](references/artifact-responsibilities.md) before
   choosing or separating diagrams. When scoped DCL materially helps readers
   understand intended or accidental complexity, apply the guidance above.
4. Label non-current material as `observed`, `inferred`, `proposed`, `blocked`,
   or `stale`; use `confirmed` where an explicit status field is useful for
   current target intent. Read
   [Authority and Evidence](references/authority-and-evidence.md) when
   reconstructing or resolving conflict.
5. Keep one authoritative home for each fact. When adjacent sources own market
   context, detailed design, implemented behavior, operations, or release
   tracking, name those boundaries and link to them instead of copying them
   into the package. Link related records directly; do not maintain a duplicate
   artifact index, trace graph, or coverage ledger.
6. Define observable acceptance for confirmed, in-scope outcomes. Then apply
   the four checks in [Change and Handoff](references/change-and-handoff.md).
7. When implementation planning is part of the request, create or update only
   the minimal external tasks or notes described above. Do not add a task
   registry, implementation plan, or ticket mirror to the PIP.

For mode-specific steps, read [Workflows](references/workflows.md). Read the
[Package Standard](references/product-intent-package-standard.md) before
creating or migrating package structure.

## Rules

- Use YAML for structured records.
- Store Mermaid in Markdown `.md` files with fenced `mermaid` blocks, including
  diagram-only files. Do not create skill-authored canonical JSON or `.mmd`.
- Give an item a stable ID only when another file needs to reference it.
- Use direct `related_ids`, `verifies`, or equivalent links where the
  relationship is meaningful. Do not duplicate all possible relationships.
- Make artifacts conditional. A missing optional artifact is not a coverage
  failure when the product does not need it.
- Do not create `governance.yaml` for a small or single-product-leader team.
  Use it only when several product authorities need explicit coordination, and
  never use its decisions to repeat the owning PIP content.
- Keep DCL optional and scoped. Do not turn it into package-wide maturity,
  completeness, readiness, or acceptance scoring.
- Follow the diagram detail boundary above. Keep each fact in the view that owns
  it and link across views instead of copying detail.
- Treat confirmed reuse or modification anchors and exact confirmed design
  references as constraints. Engineering discretion applies to unspecified
  internal choices, not to silent replacement or design deviation.
- Let engineering choose internal implementation details by default when those
  choices do not change confirmed behavior, security, privacy, data integrity,
  compatibility, reliability, operability, cost bounds, or other stated
  constraints. Do not require a discretion record for ordinary implementation.
- Treat Git as the history of ordinary edits. Only an optional multi-authority
  governance file may retain decisions, and only when authority, rationale,
  precedence, or supersession must remain visible across that team.
- Check changed YAML, direct links, status claims, and Mermaid output in
  proportion to the change. Do not add a validator or full-package test suite
  merely to perform ordinary documentation checks.
- Keep task state and implementation notes in the project's existing task
  system or working notes. Link to confirmed PIP intent; do not duplicate it or
  treat a task as product authority.
- Never treat implementation, diagrams, or agent analysis as authority. Never
  silently convert an inference or proposal into confirmed intent.
- This skill does not itself authorize product implementation or external
  writes. When implementation is separately requested, use it to preserve
  product intent and authority while the applicable engineering guidance owns
  the code work.

## Deliver

Return the requested package update or implementation-alignment result plus a
short note stating the mode, target and release boundary, task-start PIP
revision when implementation was governed by one, any material multi-authority
governance context when present, material implementation observations and their
alignment, unresolved or stale items, optional artifacts added or removed, any
material scoped DCL gaps when DCL is used, the PIP target's readiness, and
implementation alignment as separate results. When
implementation planning was requested, also return or link the minimal task set
and its proportionate verification scope without placing it inside the PIP.

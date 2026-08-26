---
name: product-intent-manager
description: Create, reconstruct, simplify, or update an explicitly requested Product Intent Package (PIP) and prepare it for product-to-implementation handoff. Use only when the user asks to work on a PIP or product-intent package; do not activate for ordinary product planning, diagramming, coding, or project documentation.
---

# Product Intent Manager

Maintain the smallest package that communicates what product to build, why it
matters, how people use it, and which observable outcomes constrain
implementation. Do not turn the package into an implementation specification
or a proof that every possible document exists.

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

## Workflow

1. Read the existing package and repository guidance. For a new package, start
   from the five-file template in `assets/product-intent-template/`.
2. Establish the target baseline and release boundary, desired outcome, actors,
   capabilities, exclusions, measures, and accountable product authority.
3. Add an artifact only when it resolves a real product, experience, behavior,
   data, system, quality, or acceptance question. Read
   [Artifact Responsibilities](references/artifact-responsibilities.md) before
   choosing or separating diagrams.
4. Label intent as `observed`, `inferred`, `proposed`, `confirmed`, `blocked`,
   or `stale`. Read [Authority and Evidence](references/authority-and-evidence.md)
   when reconstructing, resolving conflict, or seeking confirmation.
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
- Follow the diagram detail boundary above. Keep each fact in the view that owns
  it and link across views instead of copying detail.
- Treat confirmed reuse or modification anchors and exact confirmed design
  references as constraints. Engineering discretion applies to unspecified
  internal choices, not to silent replacement or design deviation.
- Let engineering choose internal implementation details by default when those
  choices do not change confirmed behavior, security, privacy, data integrity,
  compatibility, reliability, operability, cost bounds, or other stated
  constraints. Do not require a discretion record for ordinary implementation.
- Treat Git as the history of ordinary edits. Record a decision only when its
  rationale or authority matters beyond the diff.
- Check changed YAML, direct links, status claims, and Mermaid output in
  proportion to the change. Do not add a validator or full-package test suite
  merely to perform ordinary documentation checks.
- Keep task state and implementation notes in the project's existing task
  system or working notes. Link to confirmed PIP intent; do not duplicate it or
  treat a task as product authority.
- Never treat implementation, diagrams, or agent analysis as authority. Never
  silently convert an inference or proposal into confirmed intent.
- Do not implement the product as part of this skill.

## Deliver

Return the updated package plus a short note stating the mode, target and
release boundary, material decisions, unresolved or stale items, optional
artifacts added or removed, and whether handoff is confirmed or blocked. When
implementation planning was requested, also return or link the minimal task set
and its proportionate verification scope without placing it inside the PIP.

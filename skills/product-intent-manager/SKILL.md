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
- Let engineering choose internal implementation details by default when those
  choices do not change confirmed behavior, security, privacy, data integrity,
  compatibility, reliability, operability, cost bounds, or other stated
  constraints. Do not require a discretion record for ordinary implementation.
- Treat Git as the history of ordinary edits. Record a decision only when its
  rationale or authority matters beyond the diff.
- Check changed YAML, direct links, status claims, and Mermaid output in
  proportion to the change. Do not add a validator or full-package test suite
  merely to perform ordinary documentation checks.
- Never treat implementation, diagrams, or agent analysis as authority. Never
  silently convert an inference or proposal into confirmed intent.
- Do not implement the product as part of this skill.

## Deliver

Return the updated package plus a short note stating the mode, target and
release boundary, material decisions, unresolved or stale items, optional
artifacts added or removed, and whether handoff is confirmed or blocked.

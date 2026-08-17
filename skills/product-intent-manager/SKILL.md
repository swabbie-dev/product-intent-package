---
name: product-intent-manager
description: Manage a Product Intent Package for greenfield product definition, reconstruction of an existing product, completion of an incomplete package, or iteration on confirmed product intent. Use when planning actors, journeys, capabilities, behavior, design boards, system interactions, or an implementation handoff. Keep observed, proposed, confirmed, blocked, and stale intent separate. Do not implement the product or silently decide unresolved behavior.
---

# Manage Product Intent

Create a clear, reviewable Product Intent Package that explains what the
product should do, how people and systems use it, and what remains unresolved.
Work from actor goals and observable product outcomes. Keep product judgment
separate from implementation detail.

## Choose the mode

- **Create:** Start with a product idea. Define the boundary, actors, outcome,
  capabilities, journeys, and release scope.
- **Reconstruct:** Start with an existing product. Treat code, screens, tests,
  documents, analytics, runtime behavior, and operations as evidence of what
  exists. Do not treat existing behavior as desired behavior.
- **Complete:** Start with an incomplete package. Find missing actors,
  journeys, states, decisions, links, and acceptance cases. Route each gap to
  the authority who can resolve it.
- **Iterate:** Start with a requested change. Record the request, identify its
  affected actors and outcomes, update dependent artifacts, and obtain fresh
  confirmation.

## Core workflow

1. Establish the target product outcome, release boundary, actors, actor goals,
   system boundary, external systems, capabilities, exclusions, and success
   measures. Name product, design, technical, data/security/privacy,
   quality/operations, legal/compliance, and release authorities as needed.
2. Record source evidence and label every claim as observed, proposed,
   confirmed, blocked, or stale. A current implementation is observed evidence;
   it is not automatically target intent. Never turn an inference into a
   confirmed requirement.
3. After actor and capability scope, create lifecycle journeys before detailed
   flows. Each journey has phases, actor actions, product responses, outcomes,
   exceptions, recovery, and links to detailed artifacts. Read
   [Lifecycle Journey Maps](references/lifecycle-journey-maps.md) for the
   journey rules.
4. Build the product map, consolidated stack context, lifecycle journeys, user
   flows, behavior, data model, contracts, sequences, quality constraints, and
   verification. For each state machine that crosses physical services, record
   who initiates, commits, executes, observes, and recovers each transition.
   The consolidated diagram views are stack context, user flows, state
   machines, data model/ERD, sequences, and deployment only when deployment
   topology is complex. Lifecycle journeys remain semantic product records.
   Use [Product Artifact Practices](references/product-artifact-practices.md)
   for diagram selection, transition placement, sequence, and design-board
   rules.
5. Ask the accountable authority the smallest question that closes each
   build-affecting gap. Record the answer, source, affected stable IDs, and any
   explicit exclusion or bounded discretion. Do not hide uncertainty in prose.
6. When intent changes, record the new decision, mark the parent and every
   affected dependent stale, update all affected artifacts and acceptance cases,
   and obtain confirmation again. Do not restore stale intent by editing only
   the file where the change began.
7. Before handoff, confirm that every in-scope capability and journey has an
   owner, decision, evidence, detailed links, failure and recovery coverage,
   and acceptance cases. Return a confirmed handoff or a clear blocked queue.

Track the Product Intent Package in Git so its history remains reviewable.

## Working rules

- Store structured package records as YAML. Store Mermaid sources as Markdown
  `.md` files with fenced `mermaid` blocks, including diagram-only files. Keep
  canonical records human-readable in common editors.
- Use stable IDs and links. Keep one authoritative value for each fact; do not
  copy detailed rules between a journey, flow, screen, state, contract, or
  sequence.
- Use one `architecture/stack-context.md` diagram for actors, the product
  boundary, external systems, physical services, responsibilities, connections,
  and normally deployment placement. Do not create separate component,
  container, or context diagrams. Use `architecture/deployment.md` only when
  environment, region, network, failover, or rollout complexity would make the
  combined view hard to understand. Keep deployment in stack context when that
  makes its dependencies and product repercussions easier to understand. The
  separate deployment view must reuse the same stack-node IDs and must show
  affected connections or state without repeating responsibilities.
- Merge screen topology and user flows in `experience/user-flows.md`. Keep
  `SCREEN-*` records in YAML and keep design-board views as supporting records.
- Merge conceptual domain relationships and the ERD in
  `data/data-model.md`. Keep `DOM-*` and `DATA-*` IDs semantically distinct.
- Keep product outcome, release boundary, exclusions, and measures in the
  governance scope and capability records. The stack context is the sole
  context diagram.
- Name each confirmed physical service or runtime, state its responsibilities,
  and label its connections. Show security controls on the service, connection,
  or trust zone where they apply.
- A journey frames detailed artifacts. It does not replace a flow, screen,
  rule, state machine, contract, sequence, quality constraint, or acceptance
  scenario.
- Do not invent emotion, motivation, metrics, or user preference. Mark a gap
  blocked until evidence or an accountable authority resolves it.
- Do not mark a package ready while a blocking question, contradiction,
  uncovered capability, unconfirmed target, or stale dependent remains.
- Do not implement the product as part of this skill.

## Load references as needed

1. Read [Product Artifact Practices](references/product-artifact-practices.md)
   for the outward-facing artifact rules.
2. Read [Product Intent Package Standard](references/product-intent-package-standard.md)
   before creating or changing the package structure.
3. For a new product, read [Greenfield Workflow](references/greenfield-workflow.md).
4. For reconstruction, read [Reconstruction Workflow](references/reconstruction-workflow.md)
   and [Authority and Evidence Policy](references/authority-and-evidence-policy.md).
   For completion or iteration, read [Lifecycle and Change Management](references/lifecycle-and-change-management.md).
5. Read [Questioning Protocol](references/questioning-protocol.md) when an
   authority decision is needed and [Coverage and Handoff Gates](references/coverage-and-handoff-gates.md)
   before handoff.

## Deliver

Return the updated package and a brief product record stating the mode, target
and release boundary, decisions made, affected and stale artifact IDs,
unresolved questions, and whether the handoff is confirmed or blocked.

# Product Artifact Practices

Use this reference when deciding what product artifact to create, when to create
it, and how to keep it useful to people who review the product directly.

## Contents

- [Artifact order](#artifact-order)
- [Intent status](#intent-status)
- [Lifecycle journey maps](#lifecycle-journey-maps)
- [Consolidated diagram views](#consolidated-diagram-views)
- [Stack context and deployment](#stack-context-and-deployment)
- [Sequence diagrams](#sequence-diagrams)
- [Design-board organization](#design-board-organization)
- [Changes and handoff](#changes-and-handoff)
- [File format](#file-format)

## Artifact order

Create artifacts in this order. Move back when new evidence changes an earlier
decision.

| Artifact | Create when | Primary form |
| --- | --- | --- |
| Product map | The product boundary, actors, outcomes, capabilities, external systems, or exclusions are not clear. | Scope and capability registries; the context diagram is in stack context |
| Lifecycle journey | An actor, entity, task, operation, service, integration, or relationship has a meaningful lifecycle. | Journey registry in YAML plus Markdown source |
| Domain model | Terms, ownership, relationships, or lifecycle rules need a shared meaning. | Concept view in `data/data-model.md` and glossary |
| User flow | An actor must reach an outcome through paths, screens, branches, cancellation, or recovery. | Combined flow and screen-topology diagram in `experience/user-flows.md` |
| Interface model | A user-visible surface has screens, states, inputs, outputs, or responsive behavior. | Screen records, mockups, and board views linked from user flows |
| Design system | Repeated visual or interaction patterns need shared rules. | YAML tokens and component records |
| Behavior model | States, rules, permissions, timing, or side effects change the outcome. | State diagrams, rules, decision tables, and cross-service transition allocation |
| Data model | Product behavior depends on stored, derived, retained, exported, or deleted data. | Combined domain and ERD view in `data/data-model.md`, schema, and lifecycle records |
| Stack context and deployment | Responsibilities, trust boundaries, deployment, or system ownership affect the product. | `architecture/stack-context.md`; separate `architecture/deployment.md` only for complex topology |
| Contract model | An API, event, webhook, payment boundary, or external integration affects an outcome. | YAML contract records |
| Sequence diagram | The product behavior depends on ordered interactions or time between actors and systems. | `SEQ-*` artifact metadata plus Markdown Mermaid source |
| Quality model | Performance, reliability, security, privacy, accessibility, compatibility, or operations affect the outcome. | Measurable YAML constraints |
| Verification model | A capability or constraint needs observable acceptance scenarios and linked coverage. | Acceptance and traceability records |

Keep the product map and lifecycle journeys stable enough to frame the detailed
artifacts. Do not use a later technical artifact to hide an earlier product gap.

## Intent status

Use a status in the canonical record and show the same status on the design
board. A color or position may support the label, but must not be its only
meaning.

| Status | Meaning | Working rule |
| --- | --- | --- |
| `observed` | Direct evidence of the existing product, supplied research, or a recorded fact. | Preserve the source and do not present it as the desired target. |
| `proposed` | A candidate target or interpretation offered for a decision. | Show the choice and its trade-offs; ask the accountable authority. |
| `confirmed` | The accountable authority accepted the target for the stated scope. | Treat it as canonical until a later change makes it stale. |
| `blocked` | A missing authority, conflict, or missing evidence prevents a responsible decision. | Keep the gap visible and state the question that unblocks it. |
| `stale` | A previously confirmed item may be affected by a changed decision or dependency. | Review the impact and reconfirm before relying on it. |

Do not overwrite an observed record with a proposal. Do not label a proposal as
confirmed because it appears in a polished diagram. Do not remove a blocked
question to make the package appear complete. When a confirmed item becomes
stale, preserve its prior decision and identify the changed dependency.

## Lifecycle journey maps

Create a journey after the actors and capabilities are in scope and before
detailed flows, screens, rules, or technical interactions. Create one whenever
the product has a material lifecycle for:

- a customer or user relationship;
- a bounded job or task;
- an operational case or support process;
- an entity, asset, resource, or account;
- a developer or system integration;
- a service involving frontstage and backstage actors; or
- a marketplace, partner, or ecosystem relationship.

Do not use a marketing funnel as a journey unless the product authority confirms
that it is the product lifecycle being specified.

Each journey must show:

1. the actor or actors, their goal, and ownership of each handoff;
2. the trigger, scope, time axis, topology, and recurrence;
3. phases with stable local IDs and entry and exit conditions;
4. an actor action and a product response for every in-scope action;
5. state, data, or event effects and links to detailed records;
6. success, terminal, failure, pause/resume, abandonment, exit, and recovery;
7. evidence, intent status, accountable authority, and confirmation decision;
8. related flows, screens, rules, state machines, contracts, sequences,
   quality constraints, and acceptance scenarios.

Use `single_actor` only when one actor owns the relevant goal. Use
`role_specific` when materially different roles have different paths or
outcomes. Use `multi_actor_coordinated` when actors share one lifecycle and the
map must show handoffs. Split journeys when the actors, goals, time axis,
authority, or observable outcomes differ materially.

Store journey metadata in `experience/journeys/index.yaml`. Store each editable
source in `experience/journeys/JOURNEY-*.md`. The source may contain a fenced
`mermaid` diagram, a Markdown lifecycle table, or both. A file that contains
only a Mermaid diagram is still a Markdown `.md` source. Use stable IDs rather
than copying detailed behavior into the map.

## Consolidated diagram views

Keep the five default source files below. Populate each diagram when it applies,
or record a confirmed not-applicable result in coverage. Add the deployment
source only when deployment needs a separate view.

| View | Purpose | Canonical source |
| --- | --- | --- |
| Stack context | Actors, product boundary, external systems, physical services, responsibilities, connections, and normally deployment placement | `architecture/stack-context.md` |
| User flows | Actor paths, screen topology, branches, failure, and recovery | `experience/user-flows.md` |
| State machines | Valid states and transitions, including cross-service placement | `behavior/state-machines.md` |
| Data model / ERD | Conceptual domain relationships and persisted data relationships | `data/data-model.md` |
| Sequences | Ordered messages for one consequential outcome | `sequences/sequences.md` |
| Deployment | Complex environment, region, network, failover, or rollout topology | `architecture/deployment.md` only when needed |

Use `governance/scope.yaml` and `product/capabilities.yaml` for product
outcome, release boundary, exclusions, and capability records. Do not create a
second product context diagram. Stack context is the sole context diagram.

Merge screen topology into the user-flow view. Keep `SCREEN-*` details in
`experience/screens.yaml`, mockups, and the design board. Do not create a
separate canonical screen-map diagram.

Merge the conceptual domain view and ERD in `data/data-model.md`. Keep
`DOM-*` IDs conceptually distinct from persisted or derived `DATA-*` IDs. Keep
schema, lifecycle, and glossary records as supporting files.

## Stack context and deployment

Use `architecture/stack-context.md` as the one physical architecture diagram.
It combines the product context with physical clients, deployed services,
managed platforms, workers, data stores, queues, files, trust zones, and their
connections. It normally includes deployment placement when that placement is
simple enough to understand in the same view.

Create a separate `architecture/deployment.md` only when environment, region,
network, failover, or rollout complexity would make the combined view hard to
understand. Keep deployment in stack context when that makes deployment
dependencies and product repercussions easier to understand. The separate view
must reuse the same physical stack-node IDs, link to the stack context, show
affected connections or state, and avoid repeating service responsibilities.

Create a stack-context map when the product uses more than one client, deployed
service, managed platform, worker, data store, queue, file store, or external
provider. Use one node for each physical runtime or service boundary. Name the
actual provider, platform, or runtime when it is confirmed. If it is not
confirmed, show its status and route the choice to an authority or bounded
implementation-discretion record.

For each stack-context node, show:

- what is deployed there;
- the responsibilities it owns;
- the durable or ephemeral state it owns;
- the consequential security and operational controls; and
- the physical services or external systems it calls.

Label each connection with its direction, protocol or transport, and the data
or message meaning. Show synchronous, asynchronous, network, and trust
boundaries when they affect the product. Put security controls on the service,
connection, or trust zone where they apply. Do not draw a security policy as a
peer service unless it is a separately deployed service.

Do not mix logical API, event, data, and product-capability artifacts into the
stack context as if they were physical services. Link those artifacts to the
physical service that exposes, stores, or executes them. Model internal modules
only when their boundary changes ownership, deployment, trust, failure,
scaling, or an observable outcome.

Preserve an existing `ARCH-*` ID when the same responsibility moves to the
stack-context file. If one broad architecture item hides several independent
physical boundaries, keep the ID for the responsibility that still matches or
supersede it through a decision. Create new `ARCH-*` IDs only for the additional
physical boundaries. Update paths, versions, decisions, staleness, and
traceability together.

Keep each canonical state machine focused on valid states and transitions. For
each state machine that crosses physical services, add a transition-allocation
table directly below it:

| Transition | Initiator | Durable authority | Executor | Observers | Failure and recovery |
| --- | --- | --- | --- | --- | --- |
| `SM-*.transition-*` — state A to state B | actor or `ARCH-*` that requests the change | `ARCH-*` and `DATA-*` where the change becomes valid, or `none` for local state | `ARCH-*` that performs the work | actors and services that read or display it | rejected, timed-out, retry, compensation, or manual path |

Distinguish the initiator from the durable authority. A worker can request a
claim while a database transaction owns the valid state change. Link each row
to applicable `ARCH-*`, `DATA-*`, `EVT-*`, `SEQ-*`, rule, quality, and
acceptance records. In the failure and recovery cell, link the canonical rule,
transition, sequence, or acceptance record instead of copying its detailed
logic. Use a sequence diagram for the ordered messages in one outcome. Do not
use a sequence diagram as the only definition of valid states and transitions.
Give each allocated transition a stable local ID. Do not register local
transition IDs as global artifacts. Use the local ID as `source_part_id` on an
edge from the parent `SM-*` when transition-level traceability is needed.
The state diagram and allocation table in `behavior/state-machines.md` are the
canonical source; do not create a duplicate transition registry. Do not split a
state machine only because it crosses services. Split it when it describes a
different entity, lifecycle, authority, or product outcome.

## Sequence diagrams

Create a sequence diagram whenever any of these situations can change the
observable product outcome:

- a request crosses two or more systems or trust boundaries;
- an asynchronous event, queue, webhook, notification, or background worker is
  involved;
- a timeout, retry, backoff, duplicate delivery, or compensation path matters;
- authentication, authorization, session expiry, credential rotation, or
  permission changes the path;
- payment, billing, credit, entitlement, refund, or fulfilment state changes;
- work runs for a long time or reports progress after the initiating request;
- concurrent requests, idempotency, ordering, locking, or race outcomes matter;
- a failure, partial failure, rollback, recovery, or manual repair is possible;
- a person reviews, approves, escalates, supports, or hands work to another
  person; or
- a third-party provider, integration, import, export, or external callback is
  part of the outcome.

For each sequence, show the actors and systems, trust boundaries, message
order, synchronous or asynchronous behavior, state changes, payload meaning,
success result, failure result, timeout and retry behavior, duplicate and
idempotency behavior, ownership, and recovery or human handoff. Link each
important interaction to its API, event, rule, data, quality, journey, and
acceptance records. Keep the sequence focused on one observable outcome; split
unrelated interactions into separate `SEQ-*` records.

Write the sequence source in a Markdown `.md` file with a fenced `mermaid`
block. Keep message and boundary details in the linked API, event, rule, and
data records. Do not make a rendered image the only source.

## Design-board organization

Organize the board so a reviewer can move from product context to detailed
states without searching through meeting history. Use frames or sections in
this order:

1. **Index and legend:** product name, target release, board owner, last
   confirmation, stable-ID legend, status legend, and links to canonical
   records.
2. **Baseline views:** keep clearly separated sections for `as-observed`,
   `intended-current`, and `target-next`. Do not mix their cards or edges.
   Link corresponding items by stable ID and show the status and evidence for
   each view.
3. **Actors and journeys:** actor goals, actor coverage, journey phases,
   ownership, handoffs, exceptions, and journey status.
4. **Capabilities and user flows:** capability boundaries, entry points, screen
   topology, happy paths, alternate paths, permissions, cancellation, failure,
   and recovery.
5. **Screen records and states:** screen IDs, state transitions, inputs,
   outputs, mockups, and links to the combined user-flow diagram.
6. **Components and tokens:** shared components, variants, interaction states,
   content patterns, responsive rules, and design-token references.
7. **Annotations and decisions:** evidence notes, assumptions, proposals,
   confirmed decisions, open questions, contradictions, and stale items.
8. **Review and handoff:** review owner, decision queue, affected authorities,
   acceptance coverage, release boundary, and the current handoff status.
9. **Archive and reference:** superseded boards, prior decisions, source
   references, and historical context. Keep these visibly outside the active
   product model.

For reconstruction, use the three baseline views as follows:

- `as-observed` shows what the inspected product does, with evidence links;
- `intended-current` shows what the authorities want the current product to do;
- `target-next` shows the proposed next product change and its open decisions.

Never draw a direct arrow from `as-observed` to `confirmed` without an explicit
authority decision. A target change can remain proposed while the current
intent remains confirmed.

Every board item must have a stable ID, a visible status, an owner where one is
needed, and a link to its canonical record. Use the same IDs across the board,
YAML registries, Markdown diagrams, decisions, and acceptance scenarios.

For every screen or meaningful state, show the applicable loading, empty,
populated, partial, error, permission-denied, unavailable, success, and
recovery states. Show responsive and device behavior where it changes the
product outcome. Show keyboard and accessibility behavior where it changes
completion of the actor goal.

For every component, show its purpose, variants, interaction states, content
rules, responsive behavior, and accessibility constraints. Reference shared
components instead of redrawing a local variant without a decision.

Use annotations to explain rationale or link evidence; do not use annotations
as a second source for a build-affecting rule. Mark a proposed or stale item on
the board even when its visual treatment resembles a confirmed item. Keep
blocked questions next to the affected flow or state so the missing decision is
visible at review time.

## Changes and handoff

Treat every requested change as evidence until the accountable authority
confirms it. Identify the changed outcome, actor, capability, journey phase,
state, system interaction, or constraint. Review its dependent flows, screens,
components, behavior, data, contracts, sequences, quality constraints, and
acceptance scenarios.

Mark the parent and affected dependents stale before editing them. Update the
canonical records, board, diagrams, decisions, and acceptance cases together.
Restore confirmed status only after the affected authorities review the new
outcome. Preserve superseded decisions and explain the reason for the change.

Before handoff, confirm:

- every in-scope actor and capability has a lifecycle context or an explicit
  confirmed exclusion;
- every journey has actor actions, product responses, terminal outcomes,
  exception and recovery coverage, and detailed links;
- every sequence situation listed above has a focused sequence when applicable;
- every stack-context node states its responsibilities and every cross-service
  state transition has a complete transition allocation;
- a separate deployment view exists only when deployment complexity requires it,
  and it reuses stack-context node IDs without repeating responsibilities;
- every screen and component has the states and responsive behavior that affect
  the outcome;
- every item has the correct status, owner, source, and authority decision; and
- no blocking question, contradiction, unconfirmed proposal, or stale dependent
  remains in the handoff scope.

## File format

Use YAML for structured Product Intent Package records. Use Markdown `.md` for
all Mermaid source files, including diagram-only files, and wrap each diagram in
a fenced `mermaid` block. Use stable IDs and links to connect human-readable
diagrams and boards to canonical records. Preserve external evidence in its
source format and label it as evidence rather than target intent.

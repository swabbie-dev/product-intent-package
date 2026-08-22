# Artifact Responsibilities

## Selection rule

Use the smallest set of artifacts that answers the product questions at hand.
Every artifact must own distinct information. If two artifacts would explain
the same fact, keep the fact in the more appropriate owner and link to it.

The five default files establish product scope, governance, acceptance, the
physical system map, and actor flows. Add the following only when triggered:

| Optional artifact | Add when |
| --- | --- |
| Journey map | Time, phases, recurrence, roles, or handoffs add context that a focused flow cannot show |
| Screen records | Screen-specific content, actions, validation, responsive behavior, or visible states need detail beyond the flow |
| Design records | Repeated visual, content, component, interaction, responsive, or accessibility rules constrain the design handoff |
| Rules or decision table | Several conditions, priorities, permissions, or calculations select an outcome |
| State machine | A product or domain object has meaningful valid states and transitions |
| Data model / ERD | Entity identity, ownership, relationships, or cardinality affect the product |
| Schema detail | Fields or constraints are product-significant or form a shared boundary |
| API, event, or integration contract | A boundary is shared, external, compatibility-sensitive, or product-significant |
| Sequence | Ordered cross-system work, async behavior, or recovery changes an outcome |
| Quality constraints | A measurable performance, reliability, security, privacy, accessibility, compatibility, operations, or cost bound matters |
| Separate deployment view | Environment, region, network, failover, or rollout topology makes stack context hard to read |

Do not create a file merely to record `not applicable`. State a consequential
exclusion in `product.yaml` or `governance.yaml`; otherwise omit the artifact.

## Diagram responsibilities

| View | Question it owns |
| --- | --- |
| Stack context | What physical systems exist, what does each own, and how do they connect? |
| User flow | What does the actor do, see, choose, and experience next? |
| State machine | Which lifecycle states and transitions are valid? |
| Data model / ERD | What concepts or persisted entities exist, and how do they relate? |
| Sequence | Which physical systems communicate, in what order, for one consequential outcome? |

These views are enough for ordinary application work. A decision table is a
supporting logic format, not another diagram type. Deployment is usually part
of stack context and becomes separate only under the trigger above. Do not add
component, container, system-context, screen-map, domain-model, or similar
diagrams that repeat one of these views.

## One fact, one owner

| Information | Owner |
| --- | --- |
| Outcome, actors, capabilities, release boundary, exclusions, measures | `product.yaml` |
| Authority, consequential decisions, unresolved questions or conflicts | `governance.yaml` |
| Observable proof of product outcomes | `acceptance.yaml` |
| Actor action, navigation, visible outcome, and visible recovery choice | User flow |
| Detailed content and actions for a surface | Screen record, when needed |
| Condition combinations that select an outcome | Rule or decision table |
| Valid states, transitions, triggers, and guards | State machine |
| Ordered calls, events, retries, and runtime failure | Sequence |
| Physical responsibility, owned state, provider, and trust boundary | Stack context |
| Entity identity, relationship, and cardinality | Data model / ERD |
| Request, response, event, and error shape | Contract |
| Product-significant field or storage constraint | Schema detail |

## Preserve context with direct links

- A `FLOW-*` action may link to the `SEQ-*` that performs consequential work.
- A sequence uses the same `ARCH-*`, `API-*`, `EVT-*`, and `DATA-*` IDs as the
  physical and boundary records.
- A sequence ends at the same visible `SCREEN-*` outcome or durable `SM-*`
  state used by the flow or state machine.
- A state transition links to a sequence only when ordering or coordination
  matters.
- Acceptance scenarios name the `CAP-*`, `RULE-*`, `SM-*`, or other outcomes
  they verify.

Share an ID and a short label. Do not copy the selecting rule, transition
definition, or runtime messages into every view.

## User flows

A user flow owns observable experience. Include the actor goal and entry point,
actions and choices, screen topology, visible states, alternate paths,
cancellation, failure, recovery, and terminal outcomes that matter.

Treat internal system work as a black box between an actor action and a visible
response. A flow may name `access denied`, `no results`, or another product
condition, but it must not show membership lookups, API or database calls,
query mechanics, cursor handling, retries, idempotency, or internal state that
has no visible effect.

Keep one actor goal or closely related outcome in one flow. Use a short overview
and linked subflows when branches and crossing lines obscure the actor path.
Keep screen topology in the user-flow view; do not create a separate screen map.
For a headless or operator product, show actor actions and observable responses
without inventing screens.

Make each consequential user-visible surface explicit with a labeled visual
boundary such as `SURFACE · Match Feed` or, when referenced across files,
`SCREEN-001 · Match Feed`. Put the actions and visible states owned by that
surface inside its boundary, and label transitions between surfaces. This
surface-and-state inventory tells designers which pages, views, modals, panels,
or messages need mockups. Do not treat every flow node as a mockup: create a
mockup only when a surface or materially different state needs visual design.
The grouping communicates scope; it is not a wireframe.

## Sequences

A sequence owns runtime coordination for one consequential outcome. Include its
actor action or system trigger, physical `ARCH-*` participants, ordered sync or
async messages, authority and data boundaries, point of durable change, and
material timeout, retry, duplication, partial-failure, compensation, or human
recovery behavior.

Use the physical client as a participant. A `SCREEN-*` identifies the starting
or resulting surface; it is not a runtime lifeline. Return relevant facts once
and link to the rule or decision table that selects among visible outcomes
instead of repeating the same messages in many UI branches.

Split sequences only when message order, ownership, or recovery materially
differs. Do not create one for a local interface change or restate navigation,
entity relationships, or valid lifecycle states inside it.

## State machines

A state machine owns stable lifecycle states, triggers, guards, permitted and
forbidden transitions, and material failure or recovery states. Do not model
every loading or display variant as durable state when it is derived from other
facts.

When a transition crosses physical services, name where it is initiated, where
it becomes valid or durable, and which system executes or observes it. Link a
sequence when message order matters. Do not put screen navigation, database
fields, or ordered service messages in the state diagram.

## Data models and ERDs

Use one data-model view for conceptual relationships and persisted entities.
Show identity, ownership, relationships, cardinality, and product-significant
constraints. Keep conceptual `DOM-*` and persisted `DATA-*` meanings distinct
when both are needed, even if one diagram shows their mapping.

Do not use the ERD to describe navigation, message order, transition validity,
or a full database definition. Add schema detail only when fields, constraints,
retention, migration, or compatibility are product-significant.

## Stack context and deployment

Stack context is the sole system-context diagram. Show actors, the product
boundary, external systems, physical clients, deployed services, workers,
managed platforms, stores, queues, and their labeled connections. State each
node's responsibility and owned state. Name a provider or runtime only when it
is confirmed.

Place security and operational controls on the node, connection, or trust zone
where they apply. Do not draw logical APIs, events, data records, policies, or
capabilities as peer services. Show ordinary deployment placement in this view.
If a separate deployment view is necessary, reuse the same `ARCH-*` IDs and
show only the added topology without repeating responsibilities.

## Decision tables

Use one decision table when several facts select an outcome. Let it own
condition precedence and resulting `SCREEN-*`, `SM-*`, action, or refusal.
Flows show the actor-visible result, sequences return the required facts, and
acceptance scenarios test representative combinations. Do not duplicate the
condition matrix in those artifacts.

## Optional journey maps

Create a product journey only when time, phases, recurrence, role changes, or
handoffs add meaning beyond a focused user flow. Keep actor actions and product
responses at lifecycle granularity and link detailed flows rather than copying
them.

For a research-based current-state journey, follow exactly these safeguards:

1. Create it only when placing evidence across time or touchpoints reveals
   context, transitions, or handoff problems a focused flow cannot show.
2. Mark it `observed` or `inferred` and identify it as an as-observed view; do
   not present it as intended behavior.
3. Include thoughts, emotions, friction, and workarounds only when evidence
   supports them; link the source and distinguish direct evidence from
   researcher inference.
4. Keep findings and opportunities separate from candidate product responses
   and authority-confirmed decisions.

Store a journey as editable Markdown containing a lifecycle table, a fenced
Mermaid diagram, or both. Add stable IDs only for journey parts referenced by
another file.

## Design-board guidance

A design board supports review; it does not replace canonical PIP records.
Organize it so a reviewer can move through: target and legend, actors and
outcomes, journeys when used, flows, screens and states, shared patterns,
decisions and open questions, then archived material.

Show the stable ID, intent status, and canonical link on any board item that is
referenced elsewhere. During reconstruction, visibly separate as-observed,
intended-current, and target-next views. Keep blocked questions next to the
affected outcome. Never leave a build-affecting rule or decision only on the
board.

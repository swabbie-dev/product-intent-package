# Diagram Responsibilities

## Purpose

Use the smallest set of diagrams that explains how people use the product and
how the application must behave. Each diagram answers one primary question.
Repeat stable IDs for context, but do not repeat the logic behind them.

## Core diagram responsibilities

| View | Primary question | Canonical source |
| --- | --- | --- |
| Stack context | What physical systems exist, what does each own, and how do they connect? | `architecture/stack-context.md` |
| User flow | What does the actor do, see, choose, and experience next? | `experience/user-flows.md` |
| State machine | Which states and transitions are valid? | `behavior/state-machines.md` |
| Data model / ERD | Which domain concepts and persisted records exist, and how do they relate? | `data/data-model.md` |
| Sequence | Which systems communicate, in what order, to produce one consequential outcome? | `sequences/sequences.md` |

Populate a view only when it adds distinct information required to understand
or build the product. Record a confirmed not-applicable result otherwise.
Create a separate deployment diagram only when deployment complexity makes the
stack context hard to read. Do not add another diagram when one of these views
already owns the information.

A decision table is a supporting logic format, not another diagram type. Use it
when several conditions select one outcome.

## One fact, one owner

| Information | Authoritative place |
| --- | --- |
| Actor goal, action, navigation, and visible recovery choice | User flow |
| Path to a visible screen or interaction outcome | User flow |
| Detailed screen state, content, and available actions | `SCREEN-*` record |
| Condition combinations that select an outcome | Decision table, with any governing `RULE-*` linked |
| Valid states, transitions, triggers, and guards | State machine |
| Ordered calls, events, retries, and runtime failures | Sequence |
| Physical service responsibility, owned state, and trust boundary | Stack context |
| Conceptual and physical entity relationships and cardinality | Data model / ERD |
| Full field, type, constraint, and index definitions | Schema records |
| Request, response, event, and error shapes | API, event, or integration records |

## Preserve context with shared IDs

Use references as the seam between views:

- A `FLOW-*` action links to the `SEQ-*` that performs consequential system
  work.
- A sequence uses the same `ARCH-*`, `API-*`, `EVT-*`, and `DATA-*` IDs as the
  stack, interface, event, and data records.
- A sequence ends at the same visible `SCREEN-*` outcome or `SM-*` state used
  by the user flow and state machine.
- A state-machine transition links to the sequence that executes it when
  ordering or service coordination matters.
- The data model and ERD use the same `DOM-*` and `DATA-*` IDs used by rules,
  state machines, and sequences.

Share the identifier and a short outcome label. Do not copy the rule that
selects the outcome or the messages that execute it.

## User flow

The user flow owns observable experience. Include:

- the actor goal, entry point, and preconditions in actor language;
- actor actions and choices;
- screens or other interaction surfaces;
- visible loading, empty, ready, denied, success, error, and recovery outcomes;
- navigation, cancellation, retry, and exit paths; and
- user-visible consequences of a context change.

Treat consequential system work as a black box between the actor action and the
visible product response. A flow may name a product condition such as `access
denied` or `no results`, but it must not explain how the system derived it.

Do not put these details in a user flow:

- service, API, worker, or database calls;
- membership or permission lookup mechanics;
- query, cursor, ordering, pagination, or transaction mechanics;
- message retry, idempotency, or concurrency logic; or
- internal state changes that have no observable effect.

Keep one actor goal or closely related outcome in one flow. Use a short overview
with linked subflows when one diagram becomes a web of long crossing lines.

## Sequence

The sequence owns runtime coordination for one consequential outcome. Include:

- the actor action or system event that starts the operation;
- physical participants identified by `ARCH-*`;
- ordered synchronous and asynchronous messages;
- authorization, data, event, and external-system boundaries;
- the point where a state change becomes valid or durable;
- timeouts, retries, duplicate delivery, partial failure, and compensation when
  they affect the outcome; and
- the final visible outcome or state ID.

Use the physical client `ARCH-*` as a sequence participant. A `SCREEN-*` is a
starting or resulting surface reference, not a runtime participant.

Do not use a sequence as a screen map, navigation tree, state definition, ERD,
or decision table. If the same system result can produce several visible states,
return the relevant facts once and reference the decision table that selects the
visible outcome. Do not expand one alternate branch for every UI variation when
the runtime messages are the same.

Split a sequence when a different operation has a materially different message
order, ownership boundary, or recovery path. Do not create a sequence for a
local interface change that crosses no meaningful system boundary.

## State machine

The state machine owns valid lifecycle state. Include:

- stable states and terminal states;
- triggers and guards;
- allowed and forbidden transitions;
- failure, timeout, retry, and recovery states when they change the lifecycle;
  and
- cross-service transition allocation when more than one runtime participates.

Do not put screen navigation, database fields, or ordered service calls in the
state diagram. The state machine defines whether a transition is valid. A
linked sequence explains how systems execute it.

Do not create a state machine for a simple conditional branch when a rule or
decision table states the logic more clearly.

## Data model and ERD

The combined data-model view owns domain and data structure. Include:

- conceptual `DOM-*` entities and their relationships;
- persisted or derived `DATA-*` records;
- conceptual-to-physical mappings;
- the fields, keys, constraints, ownership, and tenancy needed to understand
  identity and relationships; and
- state fields when they are stored.

Do not show navigation, operation order, service messages, or valid state
transitions in the ERD. A state field may appear in an entity, but the state
machine owns its allowed transitions. Keep detailed retention, deletion,
migration, privacy, field, type, constraint, and index rules in their structured
data records.

## Stack context

The stack context owns physical placement and responsibility. Include actors and
external systems for context, but keep the focus on physical clients, services,
workers, managed platforms, stores, owned state, connections, trust boundaries,
and deployment placement.

Do not use stack context for screen navigation, operation order, entity fields,
or detailed state transitions. Sequences reuse its `ARCH-*` participants instead
of redefining what each service owns.

## Decision tables for conditional outcomes

Use one decision table when several facts select a visible outcome or allowed
action. For example:

```text
Authorized? | Data present? | Prerequisite ready? | Role | Outcome state
```

The sequence obtains or changes the facts. The decision table selects the
outcome. The user flow shows what the actor sees and can do. Reference the same
`SCREEN-*`, `SM-*`, or local outcome IDs in all three places.

## Repair an overloaded diagram

1. Assign every node, edge, and note to the view that owns the fact.
2. Move repeated logic to that authoritative view.
3. Replace removed detail with a stable-ID link and a short outcome label.
4. Split a large user flow by actor goal and a large sequence by consequential
   operation.
5. Confirm that every additional diagram answers a distinct question.

Treat this work as a representation change. Preserve confirmed behavior,
status, evidence, and stable IDs. If two diagrams disagree, record the conflict
instead of choosing one silently.

The result should let a product reviewer follow the actor experience without
understanding the implementation, while an implementation reviewer can follow
runtime work without reconstructing product navigation.

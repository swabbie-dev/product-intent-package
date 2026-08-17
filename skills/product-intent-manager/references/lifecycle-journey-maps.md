# Lifecycle Journey Maps

## Contents

- [Purpose](#purpose)
- [Lifecycle, not a marketing funnel](#lifecycle-not-a-marketing-funnel)
- [Choose a journey type](#choose-a-journey-type)
- [Actor variants](#actor-variants)
- [Time, topology, and recurrence](#time-topology-and-recurrence)
- [Journey record](#journey-record)
- [Phase and action lanes](#phase-and-action-lanes)
- [Optional lanes](#optional-lanes)
- [Failure and recovery](#failure-and-recovery)
- [Typed intent and evidence](#typed-intent-and-evidence)
- [IDs and qualified trace edges](#ids-and-qualified-trace-edges)
- [Authority and confirmation](#authority-and-confirmation)
- [Source and representation](#source-and-representation)
- [Readiness and change](#readiness-and-change)
- [Examples](#examples)

## Purpose

A Lifecycle Journey Map records how an actor moves through a product or service
over time. It connects the actor goal, product response, state or data event,
exceptions, and detailed implementation artifacts. It is a first-class
experience artifact in a Product Intent Package (PIP).

Use a journey to establish the whole lifecycle before specifying detailed flows,
screens, rules, contracts, or sequences. A journey does not replace those
artifacts. It gives them a stable context and exposes missing phases.

The canonical registry is `experience/journeys/index.yaml`. Each journey has one
editable source at `experience/journeys/JOURNEY-*.md`. Keep the source concise.
Link to stable artifact IDs instead of copying full rules or interface details.

## Lifecycle, not a marketing funnel

A lifecycle journey describes a product-relevant state, task, operation,
relationship, entity, integration, service, or ecosystem over time. It must
include an actor goal and the product response for each in-scope action.

A marketing funnel describes attention, acquisition, conversion, or campaign
performance. It is not a lifecycle journey unless the product authority confirms
that the funnel is the product lifecycle being specified. Labels such as
`awareness`, `consideration`, or `conversion` do not prove a lifecycle. Do not
reject a phase because its name is common in marketing; check its product scope,
actor action, product response, and authority decision.

## Choose a journey type

Select the smallest type that explains the lifecycle. Record the type and a
`type_rationale` in the registry.

| Type | Use when the primary subject is |
|---|---|
| `customer_relationship` | the relationship between a customer and the product |
| `job_task` | a user task with a start, progress, result, and possible retry |
| `operational_case` | a case handled by an operator, support team, or service |
| `entity_asset` | the lifecycle of an entity, asset, or resource |
| `developer_integration` | a developer or system integration from setup to operation |
| `ecosystem_marketplace` | participation across providers, partners, or a marketplace |
| `service_blueprint` | coordinated frontstage and backstage service delivery |
| `custom` | another lifecycle; include a specific authority-confirmed rationale |

Do not create several maps to force one lifecycle into a type. Split a journey
only when actors, goals, time axis, authority, or observable outcomes differ
materially. Link related journeys with normal artifact trace edges.

## Actor variants

Declare one structural variant:

- `single_actor`: exactly one actor owns the goal and performs the relevant actions;
- `role_specific`: the same lifecycle has materially different paths or outcomes
  for two or more named roles; record one actor lane per role;
- `multi_actor_coordinated`: two or more actors act in one coordinated lifecycle;
  record ownership, hand-offs, and the product response for each action.

Do not merge materially different actor journeys to make the map shorter. Every
in-scope actor must have an `actor_coverage` record in `index.yaml`. Use
`not_applicable`, `out_of_scope`, or `blocked` only with the required decision
reference.

## Time, topology, and recurrence

Declare one `time_axis`: `relationship`, `task`, `operation`,
`entity_lifecycle`, `integration`, `service_delivery`, or
`ecosystem_participation`. Declare one or more `topology` values:
`linear`, `cyclical`, `branching`, `state_based`, `recurring`, or `nested`.
Record `recurrence_model` as the trigger, interval, or explicit `not_recurring`
statement. A phase that repeats must state the condition that returns to it.
`cyclical` and `recurring` require a directed transition cycle. `branching`
requires at least two outgoing transition records from one phase.

Use `transitions` for phase changes. A complex branch must link at least one
`FLOW-*` record. A journey phase change can affect every linked flow, rule,
screen, state machine, data model, contract, sequence, quality constraint, or
acceptance scenario. The parent journey and all affected dependents become stale
until review and confirmation.

## Journey record

Store machine-readable metadata in YAML. This metadata excerpt shows the
required meanings. See `references/registry-schemas.md` for complete phase and
transition records.

```yaml
id: JOURNEY-001
title: Complete a task
journey_type: job_task
type_rationale: The actor completes a bounded task in the product.
structural_variant: single_actor
actor_ids: [ACTOR-001]
scope: Product actions from task start to terminal result.
target_view: intended_current
status: confirmed
intent_status: confirmed
initiating_trigger: Actor starts the task.
desired_outcome: The task has the confirmed result.
success_conditions: [The result is visible and persisted.]
terminal_conditions: [Completed, abandoned, or blocked.]
time_axis: task
topology: [linear]
recurrence_model: The actor may retry after a recoverable failure.
authority_id: AUTH-PRODUCT
confirmation_decision_id: DEC-001
source_refs: [EVID-001]
version: 1
source_path: experience/journeys/JOURNEY-001.md
capability_ids: [CAP-001]
exception_coverage:
  failure: {status: covered, phase_ids: [JOURNEY-001.phase-02], artifact_ids: [FLOW-001]}
  pause_resume: {status: not_applicable, decision_id: DEC-002}
  abandonment: {status: covered, phase_ids: [JOURNEY-001.phase-02], artifact_ids: [FLOW-001]}
  exit: {status: covered, phase_ids: [JOURNEY-001.phase-02], artifact_ids: [ACC-001]}
  recovery: {status: covered, phase_ids: [JOURNEY-001.phase-02], artifact_ids: [FLOW-001]}
```

The full field rules are in `references/registry-schemas.md`. Keep one
authoritative value for each field. The source Markdown can explain rationale,
but it cannot override registry metadata.

## Phase and action lanes

Each phase has a stable local ID, for example
`JOURNEY-001.phase-01`. Each action has a stable local ID, for example
`JOURNEY-001.action-01`. Local IDs are unique within the parent journey. They
are not global artifact records and do not replace `JOURNEY-*` in the artifact
index.

Each action must state all of these lanes:

1. actor action: what the actor does or decides;
2. product response: what the product shows, changes, emits, or refuses;
3. state/data/event effect: the linked `SM-*`, `DATA-*`, or `EVT-*` artifact;
4. exception and recovery disposition where applicable.

Link detailed artifacts from the action or phase. Each response artifact must
also have a `linked_artifacts` record and qualified trace edge from the same
action. A response lane must link a `FLOW-*`, `RULE-*`, `SM-*`, `DT-*`, or a
confirmed exception decision. A
journey is not a substitute for a detailed flow, screen, rule,
state machine, contract, sequence, quality, or acceptance artifact.

## Optional lanes

Add a lane only when it changes product intent. Examples include emotion,
friction, opportunity, metrics, permissions, human hand-offs, frontstage and
backstage service work, supporting systems, compliance controls, device or
physical context, cost, timing, and communication channels. Never invent an
emotion, pain point, preference, or metric. Type it as evidence, an assumption,
a decision, a question, or a contradiction, and link its source or ledger item.

## Failure and recovery

Every journey records exactly these exception categories:

- `failure`: an error, refusal, timeout, or partial failure;
- `pause_resume`: an allowed pause and how work resumes;
- `abandonment`: the actor leaves without a terminal success;
- `exit`: an explicit terminal exit or cancellation;
- `recovery`: how the actor or system returns to a usable state.

For each category, use `covered` with phase and artifact links, or use
`not_applicable`/`out_of_scope` with a confirmed decision. Do not hide an
unknown disposition in prose. If no authority has decided it, mark the journey
blocked and add a `question` intent item.
A covered category must link at least one behavior or verification artifact
from a listed phase or one of that phase's actions. A domain concept alone does
not define exception handling.

## Typed intent and evidence

Journey notes use typed items:

- `evidence`: an observed or supplied fact, linked to `EVID-*`;
- `assumption`: a proposed interpretation that needs confirmation;
- `decision`: a normalized authority decision, linked to `DEC-*`;
- `question`: an unresolved build-affecting question, linked to `Q-*`;
- `contradiction`: conflicting claims, linked to `CON-*`.

Use `observed`, `inferred`, `proposed`, or `confirmed` for `intent_status`.
Observed and inferred maps are useful during reconstruction but cannot claim
confirmed target behavior. Do not infer emotion, motivation, or desired intent
from a diagram, click path, or visual pattern. Record the source as evidence and
ask the authority or participant.

## IDs and qualified trace edges

The journey itself is the global artifact:

```yaml
- id: JOURNEY-001
  kind: lifecycle_journey
  path: experience/journeys/index.yaml#/journeys/0
```

Links to a phase or action use `source_part_id` on the parent edge:

```yaml
- from: JOURNEY-001
  source_part_id: JOURNEY-001.action-01
  relation: governed_by
  to: RULE-001
```

Every qualified local ID must belong to its parent journey. Use existing trace
relations. Use `performed_by` from an actor to the
journey and `experienced_through` from a capability to the journey. Link the
journey to detailed artifacts with the relation that matches the fact.
Every `lifecycle_journey` artifact-index record must have one matching journey
registry record, and each journey registry record must have one artifact-index
record.

## Authority and confirmation

The existing product authority confirms lifecycle intent, scope, actor goals,
outcomes, and product responses. Domain authorities still confirm facts in
their domains: design owns visual details, technical owners confirm technical
constraints, and security/privacy/legal/operations owners confirm their facts.
Do not invent a required `journey` authority domain. Record the actual authority
and `confirmation_decision_id` in the same governance records used elsewhere.
The confirmation decision must use `product_strategy` or
`capabilities_and_behavior`, name the journey in `affects`, and come from the
journey authority or an applicable recorded delegation. Actor-coverage and
exception decisions use the same product domains and must name the actor or
journey that they affect.

For reconstruction, preserve the source baseline and distinguish observed,
inferred, proposed, and confirmed records. For greenfield work, label proposed
journeys until product authority confirms them. Build-ready requires confirmed
journey intent and no open journey question, assumption, contradiction, or
stale dependent.

## Source and representation

The editable source must be a Markdown `.md` file below the package root. It may
contain a fenced `mermaid` diagram, a Markdown lifecycle table, or both. A
diagram-only file is still Markdown. Do not use `.mmd` or an image as the
canonical source.

Use a diagram first, a compact table second, and a concrete example third. Use
prose only when those forms cannot state the meaning precisely. Keep cells
short and use stable IDs instead of copied detail.

Rendered SVG or PNG files are optional derived outputs. They must not be the
only source, must not be listed as the editable `source_path`, and must not
replace the YAML registry. Preserve external source media in evidence records
with its original format.

## Readiness and change

The `journey_closure` gate passes only when every active journey has valid
metadata, actor coverage, product responses, exception dispositions, qualified
links, authority confirmation, and detailed artifact links. A journey with an
open question, assumption, contradiction, or stale dependent blocks
`build_ready`.

When a phase, action, transition, actor, outcome, or product response changes:

1. record the request as evidence;
2. obtain the correct authority decision;
3. mark the parent journey and linked dependents stale;
4. update the journey, detailed artifacts, acceptance scenarios, traceability,
   readiness, and package version;
5. review the changed package for coverage and consistency before approval.

## Examples

### Customer relationship

`JOURNEY-010` (`customer_relationship`) can cover discover, start, use,
renew, pause, and leave for one named customer actor. Each action names the
product response, such as access, reminder, renewal offer, or confirmed exit.
Do not treat an advertising funnel as this journey without product authority
confirmation.

### Operational case

`JOURNEY-011` (`operational_case`) can cover receive a support case, triage,
request information, resolve, reopen, and close. A multi-actor variant names
the customer, support agent, and automated service lanes. Timeout, escalation,
abandonment, and recovery link to flows and acceptance scenarios.

### Developer integration

`JOURNEY-012` (`developer_integration`) can cover register an application,
obtain credentials, send a request, receive an event, retry a failure, rotate
credentials, and remove the integration. API, event, sequence, security, and
quality records remain separate detailed artifacts linked from the journey.

# Registry Record Schemas

These are the minimum interoperable shapes. Additional fields are allowed when they do not duplicate canonical facts.

## Authorities

```yaml
authorities:
  - id: AUTH-PRODUCT
    name: Named person or accountable role
    roles:
      - product_owner
    contact_ref: optional
domains:
  - domain: capabilities_and_behavior
    accountable_authority_id: AUTH-PRODUCT
delegations:
  - id: DEL-001
    delegator_id: AUTH-TECH
    delegate_id: AGENT
    scope: Internal library selection for ARCH-003
    constraints:
      - No externally observable behavior change
      - Must satisfy QC-004
    decision_id: DEC-020
```

## Coverage matrix

```yaml
structures:
  - name: behavior_model
    status: covered
    artifact_ids:
      - RULE-001
      - SM-001
    decision_id: null
lenses:
  - name: billing_entitlements_quotas
    status: not_applicable
    artifact_ids: []
    decision_id: DEC-021
```

Allowed status: `covered`, `not_applicable`, `out_of_scope`, or `blocked`. `covered` requires artifact IDs. Exclusions require a confirmed decision.

## Artifact index

```yaml
artifacts:
  - id: CAP-001
    kind: capability
    label: Create project
    path: product/capabilities.yaml#/capabilities/0
    status: confirmed
    authority_id: AUTH-PRODUCT
    confirmation_decision_id: DEC-014
    source_refs:
      - EVID-003
    version: 3
    stale: false
```

Canonical kinds by prefix:

| Prefix | `kind` |
|---|---|
| `ACTOR` | `actor` |
| `CAP` | `capability` |
| `JOURNEY` | `lifecycle_journey` |
| `DOM` | `domain_concept` |
| `FLOW` | `flow` |
| `SCREEN` | `screen` |
| `MOCK` | `mockup` |
| `TOKEN` | `design_token_set` |
| `COMP` | `component` |
| `RULE` | `rule` |
| `SM` | `state_machine` |
| `DT` | `decision_table` |
| `DATA` | `data_model` |
| `ARCH` | `architecture` |
| `API` | `api_contract` |
| `EVT` | `event_contract` |
| `INT` | `integration_contract` |
| `SEQ` | `sequence` |
| `QC` | `quality_constraint` |
| `ACC` | `acceptance_scenario` |
| `DIS` | `implementation_discretion` |

## Decision

```yaml
id: DEC-014
status: confirmed
domain: capabilities_and_behavior
statement: Members with create permission may create one project per request.
authority_id: AUTH-PRODUCT
confirmed_at: '2026-08-15T12:00:00Z'
confirmation_ref: meeting:product-review-2026-08-15
source_refs:
  - EVID-003
affects:
  - CAP-001
  - RULE-001
  - ACC-001
supersedes: []
```

Decision status: `proposed`, `confirmed`, `rejected`, or `superseded`.

## Question

```yaml
id: Q-008
status: open
decision_domain: capabilities_and_behavior
question: May archived projects be restored?
why_build_affecting: Changes state machine, permissions, API, storage, and tests.
requested_authority_id: AUTH-PRODUCT
evidence_refs:
  - EVID-011
  - EVID-012
options:
  - value: 'yes'
    consequences:
      - Add restore transition and API
  - value: 'no'
    consequences:
      - Archive is terminal
blocking_artifact_ids:
  - SM-001
  - API-004
resolution_decision_id: null
```

Closed status: `resolved`, `closed`, or `superseded`.

## Contradiction

```yaml
id: CON-003
status: open
claims:
  - source_ref: EVID-011
    claim: Deletion is permanent.
  - source_ref: EVID-012
    claim: Deletion is reversible for 30 days.
requested_authority_id: AUTH-PRODUCT
affected_ids:
  - SM-001
  - DATA-004
  - ACC-021
resolution_decision_id: null
```

## Evidence

```yaml
id: EVID-011
type: runtime_observation
location: production walkthrough recording, 00:14:22
version_ref: web@commit-abc123; flags=default
captured_at: '2026-08-15T10:00:00Z'
claims:
  - Archived projects show a Restore action.
confidence: high
limitations:
  - Admin role not tested
related_ids:
  - SCREEN-008
  - SM-001
sensitive_data: none
```

## Capability

```yaml
id: CAP-001
name: Create project
actor_ids:
  - ACTOR-001
dependency_ids: []
coverage_requirements:
  domain: true
  experience: true
  behavior: true
  data: true
  architecture: true
  contracts: true
  sequence: true
  quality: true
  verification: true
coverage_exceptions: {}
```

Every false dimension except `verification` requires a confirmed exception decision in `coverage_exceptions`.

## Actor journey coverage

Use one record for every in-scope actor. Derive the required actor set from the
actor registry and capability scope; do not merge roles with different goals.

```yaml
actor_coverage:
  - actor_id: ACTOR-001
    status: covered
    journey_ids:
      - JOURNEY-001
    decision_id: DEC-001
```

Allowed status is `covered`, `not_applicable`, `out_of_scope`, or `blocked`.
`covered` requires at least one confirmed journey ID and a confirmed decision.
An exclusion requires a confirmed decision. Use `blocked` only before
build-ready, with its blocking question in the question ledger. A journey does
not replace detailed capability coverage.

## Lifecycle journey

The journey is the global artifact. Its phase and action IDs are local parts,
not separate artifact-index records.

```yaml
journeys:
  - id: JOURNEY-001
    title: Complete a task
    status: confirmed
    intent_status: confirmed
    journey_type: job_task
    type_rationale: The actor completes a bounded task.
    structural_variant: single_actor
    actor_ids:
      - ACTOR-001
    scope: Product actions from start to terminal result.
    target_view: intended_current
    initiating_trigger: Actor starts the task.
    desired_outcome: The task has its confirmed result.
    success_conditions:
      - Result is visible and persisted.
    terminal_conditions:
      - Completed
      - Abandoned
      - Blocked
    time_axis: task
    topology:
      - linear
    recurrence_model: Actor may retry after a recoverable failure.
    authority_id: AUTH-PRODUCT
    confirmation_decision_id: DEC-001
    source_refs:
      - EVID-001
    version: 1
    source_path: experience/journeys/JOURNEY-001.md
    capability_ids:
      - CAP-001
    exception_coverage:
      failure:
        status: covered
        phase_ids:
          - JOURNEY-001.phase-02
        artifact_ids:
          - FLOW-001
      pause_resume:
        status: not_applicable
        decision_id: DEC-002
      abandonment:
        status: covered
        phase_ids:
          - JOURNEY-001.phase-02
        artifact_ids:
          - FLOW-001
      exit:
        status: covered
        phase_ids:
          - JOURNEY-001.phase-02
        artifact_ids:
          - ACC-001
      recovery:
        status: covered
        phase_ids:
          - JOURNEY-001.phase-02
        artifact_ids:
          - FLOW-001
    phases:
      - id: JOURNEY-001.phase-01
        name: Start
        product_scope: inside
        actor_goal: Begin the task.
        entry_conditions:
          - Actor is eligible.
        exit_conditions:
          - Task is ready.
        touchpoint_ids:
          - SCREEN-001
        actions:
          - id: JOURNEY-001.action-01
            actor_action: Start the task.
            product_response: Show the task state.
            response_artifact_ids:
              - FLOW-001
        state_data_event_ids:
          - SM-001
        exceptions_recovery:
          failure: Show a visible start error.
          recovery: Permit a retry.
        intent_items:
          - type: decision
            decision_id: DEC-001
        linked_artifacts:
          - id: FLOW-001
            relation: experienced_through
            source_part_id: JOURNEY-001.action-01
      - id: JOURNEY-001.phase-02
        name: Complete
        product_scope: inside
        actor_goal: Finish or leave the task.
        entry_conditions:
          - Task is ready.
        exit_conditions:
          - Task is completed, abandoned, or blocked.
        touchpoint_ids:
          - SCREEN-001
        actions:
          - id: JOURNEY-001.action-02
            actor_action: Submit the task.
            product_response: Persist the result and show success or failure.
            response_artifact_ids:
              - FLOW-001
              - RULE-001
        state_data_event_ids:
          - SM-001
          - DATA-001
        exceptions_recovery:
          - Failure returns a visible error.
          - Recovery permits a retry.
        intent_items:
          - type: evidence
            ref_id: EVID-001
        linked_artifacts:
          - id: FLOW-001
            relation: experienced_through
            source_part_id: JOURNEY-001.action-02
          - id: RULE-001
            relation: governed_by
            source_part_id: JOURNEY-001.action-02
    transitions:
      - from_phase_id: JOURNEY-001.phase-01
        to_phase_id: JOURNEY-001.phase-02
        condition: Task is ready.
        complex: false
        flow_ids: []
```

Required journey fields are `id`, `title`, `status`, `intent_status`,
`journey_type`, `type_rationale`, `structural_variant`, `actor_ids`, `scope`,
`target_view`, `initiating_trigger`, `desired_outcome`, `success_conditions`,
`terminal_conditions`, `time_axis`, `topology`, `recurrence_model`,
`authority_id`, `confirmation_decision_id`, `source_refs`, `version`,
`source_path`, `capability_ids`, `exception_coverage`, `phases`, and
`transitions`. Keep `kind` and `stale` in the artifact-index record only.

Allowed `journey_type` values are
`customer_relationship`, `job_task`, `operational_case`, `entity_asset`,
`developer_integration`, `ecosystem_marketplace`, `service_blueprint`, and
`custom`. A `custom` type needs a specific authority-confirmed rationale.
Allowed `structural_variant` values are `single_actor`, `role_specific`, and
`multi_actor_coordinated`. Allowed `target_view` values are `as_observed`,
`intended_current`, and `target_next`. Allowed `intent_status` values are
`observed`, `inferred`, `proposed`, and `confirmed`. `status` keeps the normal
artifact status and is separate from `intent_status`.
`single_actor` requires exactly one actor. `role_specific` and
`multi_actor_coordinated` require at least two actors. `cyclical` and
`recurring` require a directed transition cycle. `branching` requires at least
two outgoing transition records from one phase.

The confirmation decision must use `product_strategy` or
`capabilities_and_behavior`, include the journey ID in `affects`, and come from
the journey authority or an applicable recorded delegation. Actor-coverage and
exception decisions use the same domains and must name the actor or journey
that they affect.

Each phase requires `id`, `name`, `product_scope`, `actor_goal`,
`entry_conditions`, `exit_conditions`, `touchpoint_ids`, `actions`,
`state_data_event_ids`, `exceptions_recovery`, `intent_items`, and
`linked_artifacts`. Each action requires `id`, `actor_action`,
`product_response`, and `response_artifact_ids`. The list can be empty only
when `response_exception_decision_id` names a confirmed decision. Local IDs
must start with the parent journey ID and use `.phase-` or `.action-`.
Each response artifact also requires a `linked_artifacts` record with the same
action ID and a matching qualified trace edge.

Each `linked_artifacts` record requires `id`, `relation`, and `source_part_id`.
The parent trace edge also carries `source_part_id`. It must equal a phase or
action ID in the parent journey.
The artifact index and journey registry must contain the same set of global
`JOURNEY-*` IDs.

Each journey has exactly these exception categories:
`failure`, `pause_resume`, `abandonment`, `exit`, and `recovery`. A
`covered` category requires phase and artifact links, including a qualified
link to at least one behavior or verification artifact from a listed phase or
its action. `not_applicable` and
`out_of_scope` require a confirmed decision. An unresolved category blocks
handoff.

Intent items use `evidence`, `assumption`, `decision`, `question`, or
`contradiction`. Evidence links to `EVID-*`, decisions to `DEC-*`, questions to
`Q-*`, and contradictions to `CON-*`. Build-ready rejects active assumptions,
questions, contradictions, and journeys whose `intent_status` is not
`confirmed`.

The `source_path` must be a safe relative Markdown `.md` path under the package
root. It must contain a fenced `mermaid` block or a Markdown lifecycle table.
An image or `.mmd` file is never the canonical journey source. Rendered images
are derived outputs only.

## Screen

```yaml
id: SCREEN-001
name: New project
surface: responsive_web
route_or_entry: /projects/new
flow_ids:
  - FLOW-001
inputs:
  - project_name
actions:
  - submit
  - cancel
states:
  - default
  - submitting
  - validation_error
  - network_error
  - success
responsive_rules:
  - Single column below confirmed breakpoint TOKEN-001
accessibility_rules:
  - Validation errors announced and focus moved to first invalid field
component_ids:
  - COMP-001
  - COMP-002
mockup_ids:
  - MOCK-001
copy_refs:
  - COPY-PROJECT-CREATE
```

## Rule

```yaml
id: RULE-001
scope_ids:
  - CAP-001
priority: 100
when:
  - project_name is submitted
then:
  - trim leading and trailing whitespace
  - reject empty result
exceptions: []
examples:
  - input: '  Alpha  '
    result: Alpha
  - input: '   '
    result: validation_error
```

## Quality constraint

```yaml
id: QC-001
dimension: latency
scope_ids:
  - CAP-001
  - API-001
measure: request completion latency
target: p95 <= 250 ms
load: 100 requests/second with confirmed reference data volume
verification_method: load_test
owner_authority_id: AUTH-TECH
```

## Acceptance scenario

```yaml
id: ACC-001
type: success
capability_ids:
  - CAP-001
linked_rule_ids:
  - RULE-001
given:
  - authenticated member
  - create permission
  - valid project name
when: submit create-project action once
then:
  - one project is persisted
  - response identifies project
  - event is emitted once
test_data_refs: []
```

## Traceability edge

```yaml
from: CAP-001
relation: verified_by
to: ACC-001
```

```yaml
from: JOURNEY-001
source_part_id: JOURNEY-001.action-01
relation: governed_by
to: RULE-001
```

The parent `JOURNEY-*` is the only global trace endpoint. A
`source_part_id` must be a local phase or action ID declared by that journey.
Use the existing relations; do not add a second journey-specific relation.

## Readiness gate

Add this gate to `handoff/readiness.yaml`:

```yaml
gates:
  journey_closure:
    passed: true
    evidence_refs:
      - DEC-001
```

`journey_closure` passes only when all active journeys have actor coverage,
confirmed metadata, product-response lanes, exception dispositions, qualified
trace links, detailed artifact links, safe Markdown sources, and no unresolved
journey intent. An open question, assumption, contradiction, or stale journey
dependent blocks `build_ready`.

## Implementation discretion

```yaml
id: DIS-001
scope: Internal date parsing library inside ARCH-003
allowed_choices:
  - Actively maintained library compatible with runtime
forbidden_outcomes:
  - Different accepted date formats
  - Different timezone semantics
constraints:
  - Must satisfy RULE-017 and QC-008
authority_id: AUTH-TECH
confirmation_decision_id: DEC-030
```

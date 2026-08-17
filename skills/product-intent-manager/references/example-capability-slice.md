# Example: One Fully Traced Capability Slice

This example is illustrative, not a product default.

## Capability

`CAP-001 — Create project`

```yaml
id: CAP-001
name: Create project
actor_ids:
  - ACTOR-001
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

## Lifecycle context

Before detailed flows, confirm the lifecycle that frames the capability:

```yaml
journey_ids:
  - JOURNEY-001
journey_type: job_task
journey_phase: JOURNEY-001.phase-01
product_response: Show the create-project state and validation result.
```

The journey supplies actor, phase, action, response, exception, and recurrence
context. The flow, screen, rule, state machine, data, contract, sequence,
quality, and acceptance artifacts below remain the detailed sources of truth.

## Connected structures

This illustrative slice assumes that the technical authority confirmed Vercel
and Supabase in the runtime-stack and decision records. Do not copy these
providers as a product default.

```mermaid
flowchart LR
  ACTOR_001["ACTOR-001 Member"] -->|performed_by| CAP_001["CAP-001 Create project"]
  ACTOR_001 -->|performed_by| JOURNEY_001["JOURNEY-001 Create project journey"]
  CAP_001 -->|uses_domain| DOM_001["DOM-001 Project"]
  CAP_001 -->|experienced_through| FLOW_001["FLOW-001 Project creation"]
  CAP_001 -->|experienced_through| JOURNEY_001
  JOURNEY_001 -->|"JOURNEY-001.action-01 governed_by"| RULE_001
  JOURNEY_001 -->|"JOURNEY-001.phase-01 verified_by"| ACC_001
  CAP_001 -->|experienced_through| SCREEN_001["SCREEN-001 New project"]
  CAP_001 -->|governed_by| RULE_001["RULE-001 Name validation"]
  CAP_001 -->|governed_by| SM_001["SM-001 Project lifecycle"]
  CAP_001 -->|persists_as| DATA_001["DATA-001 projects"]
  CAP_001 -->|implemented_by| ARCH_003["ARCH-003 Vercel Projects API"]
  DATA_001 -->|implemented_by| ARCH_004["ARCH-004 Supabase Postgres"]
  CAP_001 -->|exposed_by| API_001["API-001 POST /projects"]
  CAP_001 -->|executed_by| SEQ_001["SEQ-001 Create project"]
  CAP_001 -->|constrained_by| QC_001["QC-001 Create latency"]
  CAP_001 -->|verified_by| ACC_001["ACC-001 Valid create"]
  CAP_001 -->|verified_by| ACC_002["ACC-002 Invalid name"]
  CAP_001 -->|verified_by| ACC_003["ACC-003 Unauthorized"]
```

## Decision table

| Authenticated | Has create permission | Name valid | Result |
|---|---|---|---|
| no | * | * | reject unauthenticated; no write |
| yes | no | * | reject forbidden; no write |
| yes | yes | no | validation error; preserve form input |
| yes | yes | yes | create project; return project; emit event |

## State machine

```mermaid
stateDiagram-v2
  [*] --> Draft: create
  Draft --> Active: activate
  Draft --> Archived: archive
  Active --> Archived: archive
  Archived --> Active: restore
```

Runtime allocation for this cross-service state machine:

| Transition | Initiator | Durable authority | Executor | Observers | Failure and recovery |
| --- | --- | --- | --- | --- | --- |
| Start to `Draft` | `ACTOR-001` through `ARCH-003` | `ARCH-004` commits `DATA-001` | `ARCH-003` | `ACTOR-001` | A rejected transaction creates no project and returns the linked validation or permission result |
| `Draft` to `Active` | `ACTOR-001` through `ARCH-003` | `ARCH-004` commits `DATA-001` | `ARCH-003` | `ACTOR-001` and linked readers | A rejected transaction keeps `Draft` and permits the confirmed retry path |
| `Draft` to `Archived` | `ACTOR-001` through `ARCH-003` | `ARCH-004` commits `DATA-001` | `ARCH-003` | `ACTOR-001` and linked readers | A rejected transaction keeps `Draft` |
| `Active` to `Archived` | `ACTOR-001` through `ARCH-003` | `ARCH-004` commits `DATA-001` | `ARCH-003` | `ACTOR-001` and linked readers | A rejected transaction keeps `Active` |
| `Archived` to `Active` | `ACTOR-001` through `ARCH-003` | `ARCH-004` commits `DATA-001` | `ARCH-003` | `ACTOR-001` and linked readers | A rejected transaction keeps `Archived` |

## Acceptance records

```yaml
- id: ACC-001
  capability_ids:
    - CAP-001
  given:
    - authenticated member
    - create permission
    - valid unique name
  when: submit create-project action
  then:
    - one project is persisted
    - response identifies project
    - project.created is emitted once
- id: ACC-002
  capability_ids:
    - CAP-001
  given:
    - authenticated member
    - invalid name
  when: submit create-project action
  then:
    - validation error identifies name rule
    - no project is persisted
    - entered values remain available
```

The labels may be concise because the stable IDs connect the full intent. No artifact repeats all behavior.

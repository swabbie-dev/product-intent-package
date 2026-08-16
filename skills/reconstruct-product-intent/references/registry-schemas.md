# Registry Record Schemas

These are the minimum interoperable shapes. Additional fields are allowed when they do not duplicate canonical facts.

## Authorities

```json
{
  "authorities": [
    {
      "id": "AUTH-PRODUCT",
      "name": "Named person or accountable role",
      "roles": ["product_owner"],
      "contact_ref": "optional"
    }
  ],
  "domains": [
    {
      "domain": "capabilities_and_behavior",
      "accountable_authority_id": "AUTH-PRODUCT"
    }
  ],
  "delegations": [
    {
      "id": "DEL-001",
      "delegator_id": "AUTH-TECH",
      "delegate_id": "AGENT",
      "scope": "Internal library selection for ARCH-003",
      "constraints": ["No externally observable behavior change", "Must satisfy QC-004"],
      "decision_id": "DEC-020"
    }
  ]
}
```

## Coverage matrix

```json
{
  "structures": [
    {
      "name": "behavior_model",
      "status": "covered",
      "artifact_ids": ["RULE-001", "SM-001"],
      "decision_id": null
    }
  ],
  "lenses": [
    {
      "name": "billing_entitlements_quotas",
      "status": "not_applicable",
      "artifact_ids": [],
      "decision_id": "DEC-021"
    }
  ]
}
```

Allowed status: `covered`, `not_applicable`, `out_of_scope`, or `blocked`. `covered` requires artifact IDs. Exclusions require a confirmed decision.

## Artifact index

```json
{
  "artifacts": [
    {
      "id": "CAP-001",
      "kind": "capability",
      "label": "Create project",
      "path": "product/capabilities.json#/capabilities/0",
      "status": "confirmed",
      "authority_id": "AUTH-PRODUCT",
      "confirmation_decision_id": "DEC-014",
      "source_refs": ["EVID-003"],
      "version": 3,
      "stale": false
    }
  ]
}
```

Canonical kinds by prefix:

| Prefix | `kind` |
|---|---|
| `ACTOR` | `actor` |
| `CAP` | `capability` |
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

```json
{
  "id": "DEC-014",
  "status": "confirmed",
  "domain": "capabilities_and_behavior",
  "statement": "Members with create permission may create one project per request.",
  "authority_id": "AUTH-PRODUCT",
  "confirmed_at": "2026-08-15T12:00:00Z",
  "confirmation_ref": "meeting:product-review-2026-08-15",
  "source_refs": ["EVID-003"],
  "affects": ["CAP-001", "RULE-001", "ACC-001"],
  "supersedes": []
}
```

Decision status: `proposed`, `confirmed`, `rejected`, or `superseded`.

## Question

```json
{
  "id": "Q-008",
  "status": "open",
  "decision_domain": "capabilities_and_behavior",
  "question": "May archived projects be restored?",
  "why_build_affecting": "Changes state machine, permissions, API, storage, and tests.",
  "requested_authority_id": "AUTH-PRODUCT",
  "evidence_refs": ["EVID-011", "EVID-012"],
  "options": [
    {"value": "yes", "consequences": ["Add restore transition and API"]},
    {"value": "no", "consequences": ["Archive is terminal"]}
  ],
  "blocking_artifact_ids": ["SM-001", "API-004"],
  "resolution_decision_id": null
}
```

Closed status: `resolved`, `closed`, or `superseded`.

## Contradiction

```json
{
  "id": "CON-003",
  "status": "open",
  "claims": [
    {"source_ref": "EVID-011", "claim": "Deletion is permanent."},
    {"source_ref": "EVID-012", "claim": "Deletion is reversible for 30 days."}
  ],
  "requested_authority_id": "AUTH-PRODUCT",
  "affected_ids": ["SM-001", "DATA-004", "ACC-021"],
  "resolution_decision_id": null
}
```

## Evidence

```json
{
  "id": "EVID-011",
  "type": "runtime_observation",
  "location": "production walkthrough recording, 00:14:22",
  "version_ref": "web@commit-abc123; flags=default",
  "captured_at": "2026-08-15T10:00:00Z",
  "claims": ["Archived projects show a Restore action."],
  "confidence": "high",
  "limitations": ["Admin role not tested"],
  "related_ids": ["SCREEN-008", "SM-001"],
  "sensitive_data": "none"
}
```

## Capability

```json
{
  "id": "CAP-001",
  "name": "Create project",
  "actor_ids": ["ACTOR-001"],
  "dependency_ids": [],
  "coverage_requirements": {
    "domain": true,
    "experience": true,
    "behavior": true,
    "data": true,
    "architecture": true,
    "contracts": true,
    "sequence": true,
    "quality": true,
    "verification": true
  },
  "coverage_exceptions": {}
}
```

Every false dimension except `verification` requires a confirmed exception decision in `coverage_exceptions`.

## Screen

```json
{
  "id": "SCREEN-001",
  "name": "New project",
  "surface": "responsive_web",
  "route_or_entry": "/projects/new",
  "flow_ids": ["FLOW-001"],
  "inputs": ["project_name"],
  "actions": ["submit", "cancel"],
  "states": ["default", "submitting", "validation_error", "network_error", "success"],
  "responsive_rules": ["Single column below confirmed breakpoint TOKEN-001"],
  "accessibility_rules": ["Validation errors announced and focus moved to first invalid field"],
  "component_ids": ["COMP-001", "COMP-002"],
  "mockup_ids": ["MOCK-001"],
  "copy_refs": ["COPY-PROJECT-CREATE"]
}
```

## Rule

```json
{
  "id": "RULE-001",
  "scope_ids": ["CAP-001"],
  "priority": 100,
  "when": ["project_name is submitted"],
  "then": ["trim leading and trailing whitespace", "reject empty result"],
  "exceptions": [],
  "examples": [
    {"input": "  Alpha  ", "result": "Alpha"},
    {"input": "   ", "result": "validation_error"}
  ]
}
```

## Quality constraint

```json
{
  "id": "QC-001",
  "dimension": "latency",
  "scope_ids": ["CAP-001", "API-001"],
  "measure": "request completion latency",
  "target": "p95 <= 250 ms",
  "load": "100 requests/second with confirmed reference data volume",
  "verification_method": "load_test",
  "owner_authority_id": "AUTH-TECH"
}
```

## Acceptance scenario

```json
{
  "id": "ACC-001",
  "type": "success",
  "capability_ids": ["CAP-001"],
  "linked_rule_ids": ["RULE-001"],
  "given": ["authenticated member", "create permission", "valid project name"],
  "when": "submit create-project action once",
  "then": ["one project is persisted", "response identifies project", "event is emitted once"],
  "test_data_refs": []
}
```

## Traceability edge

```json
{
  "from": "CAP-001",
  "relation": "verified_by",
  "to": "ACC-001"
}
```

## Implementation discretion

```json
{
  "id": "DIS-001",
  "scope": "Internal date parsing library inside ARCH-003",
  "allowed_choices": ["Actively maintained library compatible with runtime"],
  "forbidden_outcomes": ["Different accepted date formats", "Different timezone semantics"],
  "constraints": ["Must satisfy RULE-017 and QC-008"],
  "authority_id": "AUTH-TECH",
  "confirmation_decision_id": "DEC-030"
}
```

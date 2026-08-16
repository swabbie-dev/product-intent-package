# Greenfield Product-Intent Workflow

## Goal

Construct a complete Product Intent Package from an originator’s idea without filling gaps through agent assumptions.

## Phase 0 — Establish governance

Confirm:

- product originator and final product authority;
- named/delegated authorities for product, design, technical, data/security/privacy, quality/operations, legal/compliance, and release acceptance;
- target version and release boundary;
- decision cadence and confirmation mechanism;
- whether the agent has any bounded delegated authority.

Initialize the package with:

```bash
python scripts/init_product_intent.py <destination> \
  --name "<product>" \
  --target-version "<version>" \
  --baseline greenfield
```

## Phase 1 — Product boundary

Elicit and confirm:

- target users/actors and their goals;
- target outcome and success measures;
- system boundary and external actors/systems;
- capability map;
- release scope, priorities, and exclusions;
- confirmed constraints and non-goals.

Render product context and capability map before detailed flows. Do not proceed with an unstable boundary unless later work is explicitly exploratory.

## Phase 2 — Domain model

Elicit and confirm:

- canonical vocabulary;
- conceptual entities and identity;
- ownership, tenancy, relationships, and cardinality;
- invariants and lifecycle concepts;
- sensitive or regulated concepts.

Keep storage design separate until domain intent is stable.

## Phase 3 — Experience model

For each actor/capability:

1. map entry points and preconditions;
2. map happy, alternate, cancellation, invalid, permission, failure, and recovery paths;
3. derive screen topology;
4. enumerate screen states;
5. create low-fidelity mockups;
6. define tokens/components/interactions;
7. refine mockups and obtain design/product confirmations.

A mockup without state and behavior links is incomplete.

## Phase 4 — Behavior model

For each domain object and capability:

- build state machines;
- define triggers, guards, side effects, and terminal states;
- create decision tables for combined conditions;
- define time, ordering, duplicates, idempotency, concurrency, retry, cancellation, and compensation behavior;
- define permissions and account-state behavior;
- confirm business rules with the correct authority.

## Phase 5 — Data and technical model

With technical and data authorities:

- map domain concepts to storage entities;
- define data lifecycle, privacy, retention, export, deletion, audit, migrations, and seed data;
- define system context, containers, components, trust boundaries, and deployment;
- define every API/event/integration contract;
- define consequential sequences and failure semantics;
- define measurable quality and operational constraints.

Technical recommendations remain proposals until the technical authority confirms them or delegates the domain.

## Phase 6 — Verification and traceability

For every capability and constraint:

- create acceptance scenarios for success, invalid input, permission, failure, recovery, and boundary cases;
- link all applicable structures through traceability;
- identify any false coverage dimension and obtain a confirmed exception decision;
- confirm observable results with product/design/technical authorities as applicable.

## Phase 7 — Closure and handoff

Apply all handoff gates, run draft validation, resolve every issue, stamp the content hash, obtain and record final release/product approval for that hash, set the package to build-ready, and run final validation. Do not hand off a package with open decisions under the theory that the coding agent can “figure them out.”

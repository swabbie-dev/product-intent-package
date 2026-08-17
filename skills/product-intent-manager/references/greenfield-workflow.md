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

Copy `assets/product-intent-template/` to the product workspace. Set the product
name, target version, and `greenfield` baseline in `manifest.yaml`.

## Phase 1 — Product boundary

Elicit and confirm:

- target users/actors and their goals;
- target outcome and success measures;
- system boundary and external actors/systems;
- capability map;
- release scope, priorities, and exclusions;
- confirmed constraints and non-goals.

Render product context and capability map before detailed flows. Do not proceed with an unstable boundary unless later work is explicitly exploratory.

## Phase 2 — Lifecycle journey model

After product boundary and actor/capability scope are confirmed, map each
material lifecycle before writing detailed flows:

- select a journey type and record its rationale;
- choose single-actor, role-specific, or multi-actor-coordinated structure;
- define the time axis, topology, recurrence, trigger, outcome, and terminal
  conditions;
- divide the lifecycle into phases with stable local IDs;
- record each actor action and the product response;
- cover failure, pause/resume, abandonment, exit, and recovery;
- link each response to detailed artifacts and route complex branches to FLOW
  records;
- label the journey observed, inferred, proposed, or confirmed and obtain
  product-authority confirmation.

Do not use a journey to replace detailed flows, screens, rules, state machines,
contracts, sequences, quality constraints, or acceptance scenarios. A proposed
or unresolved journey blocks build-ready handoff.

## Phase 3 — Domain model

Elicit and confirm:

- canonical vocabulary;
- conceptual entities and identity;
- ownership, tenancy, relationships, and cardinality;
- invariants and lifecycle concepts;
- sensitive or regulated concepts.

Keep storage design separate until domain intent is stable.

## Phase 4 — Experience model

For each actor/capability:

1. map entry points and preconditions;
2. map happy, alternate, cancellation, invalid, permission, failure, and recovery paths;
3. derive screen topology;
4. enumerate screen states;
5. create low-fidelity mockups;
6. define tokens/components/interactions;
7. refine mockups and obtain design/product confirmations.

A mockup without state and behavior links is incomplete.

## Phase 5 — Behavior model

For each domain object and capability:

- build state machines;
- define triggers, guards, side effects, and terminal states;
- for each state machine that crosses physical services, record the initiator,
  durable authority, executor, observers, and failure or recovery path for each
  transition;
- create decision tables for combined conditions;
- define time, ordering, duplicates, idempotency, concurrency, retry, cancellation, and compensation behavior;
- define permissions and account-state behavior;
- confirm business rules with the correct authority.

## Phase 6 — Data and technical model

With technical and data authorities:

- map domain concepts to storage entities;
- define data lifecycle, privacy, retention, export, deletion, audit, migrations, and seed data;
- define system context and the physical runtime stack, including deployment,
  environment, and trust zones;
- name each confirmed provider or runtime, state each physical service's
  responsibilities and owned state, and label every physical connection;
- define every API/event/integration contract;
- define consequential sequences and failure semantics;
- define measurable quality and operational constraints.

Technical recommendations remain proposals until the technical authority confirms them or delegates the domain.

## Phase 7 — Verification and traceability

For every capability and constraint:

- create acceptance scenarios for success, invalid input, permission, failure, recovery, and boundary cases;
- link all applicable structures through traceability;
- identify any false coverage dimension and obtain a confirmed exception decision;
- confirm observable results with product/design/technical authorities as applicable.

## Phase 8 — Closure and handoff

Apply all handoff gates and review the package with the accountable authorities.
Resolve every material issue, record final release and product approval for the
package version, and set the package to build-ready. Do not hand off a package
with open decisions under the theory that the coding agent can “figure them
out.”

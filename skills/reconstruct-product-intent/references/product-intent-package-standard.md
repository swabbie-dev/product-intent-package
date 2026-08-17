# Product Intent Package Standard

## Purpose

A **Product Intent Package (PIP)** is a versioned, authority-confirmed, closed-world specification of **what product to build and how it must behave**, plus the technical constraints and contracts required to implement it.

The target consumer is a coding-agent orchestrator. A handoff-ready package must let that orchestrator build the product without asking what the product owner, product manager, designer, or technical authority intended.

“Closed-world” means every build-affecting detail is one of:

1. explicitly specified and confirmed;
2. explicitly excluded or not applicable;
3. explicitly delegated as bounded implementation discretion.

Anything else is an unresolved gap.

## Format version

This standard defines Product Intent Package format `3.0.0`.
`manifest.yaml` must set `schema_version: 3.0.0`. This breaking version adds
first-class lifecycle journey records, actor coverage, qualified local links,
and the `journey_closure` readiness gate.

## Non-negotiable invariants

1. **Intent is never inferred into existence.** Evidence may support a proposal; only an authorized confirmation makes it canonical.
2. **One fact, one source of truth.** Reuse stable IDs and links instead of restating the same rule in multiple artifacts.
3. **Every canonical item is governed.** It has a stable ID, status, authority, confirmation decision, version, source references, and staleness state in `governance/artifact-index.yaml`.
4. **Observed behavior is not automatically desired behavior.** Code, tests, screenshots, analytics, documents, and runtime behavior are evidence.
5. **No silent conflict resolution.** Contradictions are routed to the accountable authority and recorded as decisions.
6. **No silent defaults.** “Standard behavior” is a proposal unless an authority delegates that decision domain.
7. **Every in-scope capability is traceable.** It connects to all applicable experience, behavior, data, architecture, contract, sequence, quality, and verification artifacts.
8. **Every exclusion is deliberate.** `out_of_scope`, `not_applicable`, and waived coverage require an authority-confirmed decision.
9. **Changes propagate.** A changed decision marks all dependent artifacts stale until reviewed and reconfirmed.
10. **Build-ready is a gate, not a tone.** The package is not handoff-ready while any blocking question, contradiction, stale artifact, placeholder, missing authority, or uncovered capability remains.

## Representation rule

Prefer, in order:

1. executable schema or contract;
2. diagram or model;
3. decision table or matrix;
4. concrete example;
5. prose only when the intent cannot be represented precisely above.

Use stable IDs inside diagrams and registries. Prose explains rationale; it must not be the only location of a build-critical rule.

## Human-readable package file format

Use these rules for every Product Intent Package:

- Store every skill-authored structured package record in YAML in a `.yaml` file.
- Use unique string keys. Do not use YAML aliases or custom tags.
- Store every Mermaid diagram in a Markdown `.md` file, including files that contain only a diagram. Wrap each diagram in a fenced `mermaid` block so common editors can render it.
- Do not create canonical `.json` or `.mmd` package files.
- Preserve the original format for copied source evidence and for media types or file formats required by an external system. Record these files through `governance/evidence.yaml`; do not list them as canonical paths in `governance/artifact-index.yaml`. Preserve media types such as `application/json` when an HTTP boundary requires them.

## Canonical directory map

| Intent dimension | Canonical structures | Default files |
|---|---|---|
| Governance | authority, scope, structure/lens coverage, decisions, questions, contradictions, evidence, artifact registry, change history | `governance/*` |
| Product map | actors, system boundary, capabilities, external systems, exclusions | `product/context.md`, `product/capabilities.yaml`, `governance/scope.yaml` |
| Lifecycle journey | actor lifecycle, phases, actions, product responses, exceptions, recurrence, and dependent detail | `experience/journeys/index.yaml`, `experience/journeys/JOURNEY-*.md` |
| Domain model | conceptual entities, relationships, ownership, invariants, vocabulary | `product/domain-model.md`, `governance/glossary.yaml` |
| User-flow model | actor goals, entry points, paths, alternatives, recovery | `experience/user-flows.md` |
| Interface model | surface topology, screens, states, responsive behavior, copy references, mockups | `experience/screen-map.md`, `experience/screens.yaml`, `experience/mockups/` |
| Design system | tokens, components, variants, interaction and motion patterns | `experience/design-tokens.yaml`, `experience/components.yaml` |
| Behavior model | state machines, rules, guards, priorities, decision tables | `behavior/state-machines.md`, `behavior/rules.yaml`, `behavior/decision-tables.csv` |
| Data model | physical entities, fields, constraints, lifecycle, retention, migration | `data/erd.dbml`, `data/schema.yaml`, `data/lifecycle.yaml` |
| System architecture | context, containers, components, deployment and trust boundaries | `architecture/*.md` |
| Interface contracts | APIs, events, webhooks, third-party boundaries, errors and versioning | `contracts/openapi.yaml`, `contracts/events.yaml`, `contracts/integrations.yaml` |
| Runtime interactions | ordering, transactions, async work, failures, compensation, retries | `sequences/sequences.md` |
| Quality constraints | measurable performance, reliability, security, privacy, accessibility, compatibility, operations | `quality/constraints.yaml` |
| Verification model | acceptance scenarios and complete cross-artifact traceability | `verification/acceptance.yaml`, `verification/traceability.yaml` |
| Handoff contract | allowed implementation discretion and readiness result | `handoff/implementation-discretion.yaml`, `handoff/readiness.yaml` |

Large products may split any file by stable ID. The semantics and registry remain unchanged.

## Stable ID vocabulary

Recommended prefixes:

| Prefix | Kind |
|---|---|
| `ACTOR` | user, operator, service, or external actor |
| `CAP` | capability |
| `JOURNEY` | lifecycle journey map |
| `DOM` | domain concept |
| `FLOW` | user or operational flow |
| `SCREEN` | screen, page, view, or interaction surface |
| `MOCK` | mockup or prototype |
| `TOKEN` | design-token set |
| `COMP` | interface component or pattern |
| `RULE` | business or system rule |
| `SM` | state machine |
| `DT` | decision table |
| `DATA` | persisted entity, schema, or lifecycle model |
| `ARCH` | architecture element or diagram |
| `API` | request/response contract |
| `EVT` | event contract |
| `INT` | external integration contract |
| `SEQ` | sequence or runtime interaction |
| `QC` | quality constraint |
| `ACC` | acceptance scenario |
| `DEC` | confirmed decision |
| `Q` | unresolved question |
| `CON` | conflicting claims awaiting authority resolution |
| `EVID` | evidence item |
| `DIS` | implementation-discretion grant |

IDs are immutable. Renames change labels, not IDs. Superseded items retain their IDs in history.

## Artifact metadata

Every logical artifact is registered in `governance/artifact-index.yaml`:

```yaml
id: CAP-001
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

Allowed working statuses:

- `observed`: directly found in evidence; not yet confirmed as target intent;
- `hypothesis`: plausible interpretation; never canonical at handoff;
- `proposed`: presented for authority decision;
- `confirmed`: canonical target intent;
- `blocked`: cannot be resolved without authority or missing evidence;
- `out_of_scope`: deliberately excluded by confirmed decision;
- `not_applicable`: deliberately inapplicable by confirmed decision;
- `superseded`: historical item replaced by another item.

Only active `confirmed`, `out_of_scope`, and `not_applicable` items may remain at build-ready handoff. Historical superseded items may remain outside the active graph.

## The thirteen required information structures

### 1. Product map

Must define:

- target product outcome and release boundary;
- actors and their goals;
- product/system boundary;
- major capabilities;
- external systems and major inputs/outputs;
- explicit exclusions.

Primary form: context diagram + capability registry + scope registry.

### 2. Lifecycle journey model

For each in-scope actor, define the confirmed lifecycle context for applicable
capabilities before detailed flows:

- journey type and rationale;
- actor variant, actor lanes, scope, target view, and intent status;
- time axis, topology, recurrence, trigger, desired outcome, and terminal states;
- phases with entry/exit conditions and local IDs;
- actor actions, product responses, state/data/event effects, and detailed links;
- failure, pause/resume, abandonment, exit, and recovery dispositions;
- transitions and detailed flows for complex branches;
- authority, confirmation decision, evidence, and source Markdown path.

Primary form: `experience/journeys/index.yaml` plus editable Markdown sources
with a fenced `mermaid` block, a Markdown lifecycle table, or both. A journey
frames detailed artifacts; it does not replace a flow, screen, rule, state
machine, contract, sequence, quality, or acceptance artifact.

### 3. Domain model

Must define conceptual entities independently of storage:

- canonical vocabulary;
- identity and ownership;
- relationships and cardinality;
- invariants;
- lifecycle concepts;
- tenancy and boundary rules where applicable.

Primary form: concept/relationship diagram + glossary.

### 4. User-flow model

For every actor goal, define:

- entry point and preconditions;
- happy path;
- alternate paths;
- cancellation and undo;
- failure and recovery;
- permission and account-state branches;
- terminal outcomes.

Primary form: flow diagrams keyed by `FLOW-*` IDs.

### 5. Interface model

For every user-visible surface, define:

- navigation/topology;
- inputs, outputs, actions, and validation;
- loading, empty, populated, partial, error, permission-denied, unavailable, and success states as applicable;
- responsive and device behavior;
- keyboard and accessibility behavior;
- content/copy source;
- mockup or prototype reference.

Primary form: screen map + screen-state registry + mockups.

### 6. Design system

Define:

- tokens: color roles, typography, spacing, sizing, radius, elevation, motion;
- layout/grid and responsive rules;
- components and variants;
- interaction states;
- content and icon conventions;
- accessibility constraints;
- theming/branding rules.

Primary form: machine-readable tokens + component/interaction catalog. Mockups must reference these components rather than redefine them.

### 7. Behavior model

Define:

- object and workflow states;
- allowed transitions, triggers, guards, side effects, and terminal states;
- business rules and invariants;
- decision precedence and conflict handling;
- time, ordering, idempotency, duplicate, concurrency, retry, and cancellation semantics;
- decision tables for combinatorial conditions.

Primary form: state machines + rules registry + decision tables.

### 8. Data model

Define:

- persisted and derived data;
- fields, types, constraints, relationships, and indexes where consequential;
- data ownership and tenancy;
- creation, update, archival, deletion, retention, export, and audit behavior;
- migration, bootstrap, and seed requirements;
- privacy classification.

Primary form: ERD/DBML + schema registry + lifecycle matrix.

### 9. System architecture

Define:

- system context and external dependencies;
- deployable containers/services;
- internal components and responsibility boundaries;
- sync/async boundaries;
- trust boundaries and security zones;
- storage, queues, cache, search, jobs, and files;
- deployment topology, environments, and configuration boundaries;
- build-vs-buy decisions that affect behavior or constraints.

Primary form: context, container, component, and deployment diagrams.

### 10. Interface contracts

For every boundary, define:

- request, response, event, webhook, or file shape;
- authentication and authorization;
- errors and failure semantics;
- validation and limits;
- idempotency, pagination, filtering, ordering, and concurrency behavior;
- versioning and compatibility;
- retry, timeout, and rate-limit expectations.

Primary form: OpenAPI-compatible contract, event registry, and integration contract registry.

### 11. Runtime interaction model

Create sequence diagrams wherever ordering or component coordination matters, including:

- multi-component operations;
- transactions;
- asynchronous processing;
- external side effects;
- retries, timeouts, compensation, and dead-letter behavior;
- authentication/authorization boundaries;
- race conditions and concurrency control.

Primary form: sequence diagrams keyed by `SEQ-*` IDs.

### 12. Quality constraints

Every constraint must be measurable or testable. Cover applicable dimensions:

- latency, throughput, capacity, and scale;
- availability, durability, backup, recovery point, and recovery time;
- security, privacy, abuse resistance, and compliance;
- accessibility;
- supported devices, browsers, platforms, locales, and time zones;
- observability, auditability, supportability, and operational ownership;
- cost or resource ceilings where they constrain implementation.

Primary form: constraint matrix keyed by `QC-*` IDs.

### 13. Verification model

Define:

- acceptance scenarios for every capability, rule, failure branch, permission branch, and quality constraint;
- test data and expected results where consequential;
- tolerances for non-deterministic or numerical behavior;
- cross-artifact traceability.

Primary form: acceptance registry + traceability graph.

## Coverage lenses

The thirteen structures are canonical. Apply these lenses across them so common omissions do not hide between documents:

- roles, permissions, tenancy, and delegated access;
- onboarding, authentication, account recovery, suspension, and deletion;
- administration, moderation, support, audit, and operator workflows;
- billing, entitlements, quotas, and plan changes where applicable;
- notifications, preferences, delivery failures, and unsubscribe behavior;
- search, filtering, sorting, pagination, and empty results;
- files, import/export, migration, and interoperability;
- analytics, event instrumentation, attribution, and experiment behavior;
- localization, time zones, currencies, units, and numeric precision;
- offline behavior, poor connectivity, partial failure, and resumption;
- concurrency, duplicates, ordering, idempotency, and race conditions;
- data privacy, retention, deletion, legal holds, and user export;
- accessibility, keyboard, screen-reader, contrast, and reduced-motion behavior;
- environments, configuration, secrets, deployment, rollback, and disaster recovery.

Each lens must be either represented, explicitly not applicable, or out of scope by confirmed decision.

## Traceability model

`verification/traceability.yaml` is the package graph. Each edge is directional.
An edge from a journey to one of its local phases or actions includes
`source_part_id`; local IDs are not global artifact-index entries:

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

Canonical relations:

| Relation | Meaning |
|---|---|
| `performed_by` | actor performs or participates in the target item |
| `uses_domain` | item depends on a domain concept |
| `experienced_through` | capability is realized by a flow, screen, mockup, or component |
| `governed_by` | item is constrained by a rule, state machine, or decision table |
| `uses_data` / `persists_as` | item reads, writes, or maps to a data model |
| `implemented_by` | item is assigned to an architecture element |
| `exposed_by` | item crosses an API, event, or integration contract |
| `executed_by` | item has a runtime sequence |
| `constrained_by` | item is subject to a quality constraint |
| `verified_by` | item is proven by an acceptance scenario |
| `depends_on` | item cannot operate without another item |
| `supersedes` | item replaces a prior item |

Use `performed_by` from an actor to a journey and `experienced_through` from a
capability to a journey when the lifecycle frames that actor experience. Link
journey phases and actions with `source_part_id` on the parent journey edge.

`governance/coverage-matrix.yaml` separately proves that all thirteen canonical
structures and every cross-cutting coverage lens are either covered, confirmed
not applicable, confirmed out of scope, or blocked.

Every in-scope capability declares which coverage dimensions apply. A false dimension requires a confirmed exception decision. Every true dimension requires at least one matching traceability edge.

## Implementation discretion

The coding orchestrator may make a choice only when:

1. the choice is not externally observable **or** its observable bounds are fully specified;
2. the choice falls within a confirmed `DIS-*` grant;
3. the choice satisfies all linked quality, security, data, and compatibility constraints.

A grant must name its scope, allowed choices or principles, forbidden outcomes, constraints, authority, and confirmation decision. “Use best practices” alone is not a usable grant.

## Package target baseline

A package represents one declared target:

- `greenfield`: no existing implementation defines the baseline;
- `as_implemented`: faithfully reproduce current runtime behavior, including known quirks explicitly accepted as target behavior;
- `intended_current`: represent the product that authorities currently intend, correcting accidental implementation behavior;
- `target_next`: represent a future product version.

Never mix baselines silently. Existing-state evidence remains linked, but the canonical target is singular.

## Build-ready definition

A package is build-ready only when:

- all required authority domains have accountable owners or explicit delegations;
- scope and target baseline are confirmed;
- every in-scope capability is confirmed and fully traced across all applicable dimensions;
- every in-scope actor has journey coverage, and every active journey has
  confirmed metadata, product-response lanes, exception dispositions, and
  detailed artifact links;
- every user-visible and operational path has defined states, errors, permissions, and recovery;
- every behavior-affecting rule and lifecycle is explicit;
- every data and system boundary has a contract;
- every consequential runtime interaction has ordering and failure semantics;
- every quality constraint is measurable;
- every capability and constraint has acceptance coverage;
- all contradictions are resolved;
- no blocking questions, unresolved contradictions, placeholders, stale artifacts, or unconfirmed active items remain;
- no open journey question, assumption, contradiction, or stale journey
  dependent remains;
- every unspecified choice is covered by a bounded discretion grant;
- deterministic validation passes;
- the accountable product authority confirms the final handoff version.

A package that fails any condition is still useful, but it must be labeled
`modeled` or `blocked`, never `build_ready`.

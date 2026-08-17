# Existing-Project Reconstruction Workflow

## Goal

Convert an existing software project into one authority-confirmed target Product Intent Package. The work includes code, databases, tests, documents, tickets, mockups, media, runtime behavior, analytics, and stakeholder knowledge.

Do not produce a prettier codebase description. Reconstruct the product intent, expose every gap, and obtain decisions from the correct authorities.

## Phase 0 — Declare the target

Before modeling, obtain confirmation of:

- product and target version;
- target baseline: `as_implemented`, `intended_current`, or `target_next`;
- environments/versions that count as source evidence;
- rebuild, migration, documentation, audit, or modernization purpose;
- release boundary and known exclusions;
- accountable authorities and interview access.

If the target baseline is unclear, stop canonicalization. The same evidence can imply different packages.

## Phase 1 — Source inventory

Inventory without interpreting intent:

- repositories, branches, tags, commits, submodules;
- running environments and feature flags;
- design files, screenshots, video, prototypes, style systems;
- schemas, migrations, seed data, fixtures;
- API/event contracts and integration docs;
- product documents, tickets, decisions, roadmaps, release notes;
- test suites and QA cases;
- analytics events, logs, alerts, incident history;
- support cases, user research, and operational runbooks;
- named stakeholders and decision domains.

Run `scripts/inventory_existing_project.py` when filesystem access is available. Import the generated inventory as an `EVID-*` source; do not treat heuristic classifications as intent.

## Phase 2 — Observe the product

For each actor and reachable capability:

1. record entry points, preconditions, and environment;
2. capture the happy path;
3. force alternate, empty, loading, invalid, permission, timeout, partial-failure, and recovery states;
4. inspect responsive, keyboard, accessibility, and account-state behavior;
5. record requests, events, storage mutations, background work, and external side effects when accessible;
6. label each finding `observed`, with evidence and limits.

Observation is incomplete by definition. Do not infer unobserved branches from apparent patterns.

## Phase 3 — Analyze implementation structure

Map:

- domain concepts implied by code and data;
- routes, screens, components, and states;
- rules, state machines, validation, permissions, and feature flags;
- data entities, constraints, lifecycle, and migrations;
- architecture containers/components and trust boundaries;
- APIs, events, integrations, jobs, queues, cache, files, and search;
- sequences for consequential operations;
- quality settings, tests, monitoring, deployment, backups, and recovery.

Register every finding as evidence-backed `observed` or `hypothesis`. A clean architecture inferred from messy code is still a proposal.

## Phase 4 — Reconstruct lifecycle journeys

After source inventory and actor/capability scope, map each material lifecycle
before detailed flows:

- choose the smallest journey type and record its rationale;
- separate one actor, role-specific, and multi-actor-coordinated journeys;
- define trigger, actor goals, product responses, time axis, topology,
  recurrence, outcomes, and terminal conditions;
- preserve only observed phases and actions as observed evidence;
- mark inferred links and proposed target behavior explicitly;
- record failure, pause/resume, abandonment, exit, and recovery dispositions;
- link phases and actions to detailed artifacts without promoting local IDs to
  global artifact records;
- route missing or conflicting product responses to the product authority.

Do not infer emotion, motivation, or desired intent from a diagram, screenshot,
click path, or repeated implementation pattern. A rendered image is evidence;
the editable journey source is a Markdown file. The product authority confirms
lifecycle intent. Other authorities confirm facts in their own domains.

## Phase 5 — Build an as-observed model

Construct all thirteen structures, including lifecycle journeys, using observed
evidence. Keep these distinctions explicit:

| Layer | Meaning |
|---|---|
| observed implementation | what evidence directly shows |
| interpretation | what the agent thinks connects the evidence |
| proposed target | what the agent recommends the package should specify |
| confirmed target | what the accountable authority approved |

Do not collapse the layers.

## Phase 6 — Gap and contradiction matrix

Compare every structure and coverage lens. Create `Q-*` records for:

- missing branches, states, permissions, and error behavior;
- inconsistent code, tests, docs, mockups, and runtime behavior;
- apparent bugs that may or may not be intended;
- dead or unreachable capabilities;
- duplicate concepts or competing data models;
- undocumented feature flags and environment differences;
- implicit limits, timing, ordering, concurrency, and retries;
- missing security, privacy, accessibility, operational, and quality decisions;
- implementation details that leak into user behavior;
- facts no named authority owns.

Group questions by authority and capability. Include affected artifacts and implementation risk.

## Phase 7 — Stakeholder reconstruction interviews

Interview in evidence-first order:

1. product originator/owner: target, users, outcomes, scope, priorities, product tradeoffs;
2. product manager: capability definitions, flows, rules, edge cases, release boundaries, acceptance;
3. designer: information architecture, screen states, components, visual rules, responsive/accessibility behavior;
4. technical lead: architecture intent, data, contracts, constraints, operations, known accidental behavior;
5. domain/security/privacy/legal/operations authorities as required.

For each topic:

- show the observed model and conflicts;
- ask whether observed behavior is target behavior, defect, legacy constraint, or out of scope;
- normalize the answer into a diagram/table/schema/contract;
- obtain confirmation if normalization added interpretation;
- record the decision and propagate changes.

Use `references/stakeholder-interviews.md` for domain-specific question prompts.

## Phase 8 — Canonicalize the target

Move only confirmed items into active target intent. For each active artifact:

- assign authority and confirmation decision;
- link evidence;
- update version and staleness;
- link through traceability;
- supersede conflicting historical items without deleting evidence.

Do not preserve implementation accidents unless the authority explicitly chooses them as target behavior.

## Phase 9 — Close the package

Apply the coverage and handoff gates. Run draft validation:

```bash
python scripts/validate_product_intent.py <package-directory>
```

Resolve every error. Then stamp the final product content:

```bash
python scripts/stamp_package_hash.py <package-directory>
```

Obtain and record final approval from the release/product authority for that exact hash, set the package to build-ready, and run final validation. If any authority is unavailable or any build-affecting question remains, deliver a blocked package plus the exact decision queue.

## Required deliverables

- complete Product Intent Package directory;
- evidence inventory and source map;
- contradiction/gap register;
- authority interview/decision ledger;
- readiness report;
- explicit statement of target baseline;
- final approval or blocked-handoff report.

# Coverage and Handoff Gates

## Gate model

The package advances through five states:

| State | Meaning |
|---|---|
| `inventory` | sources and authorities are being discovered |
| `modeled` | structures exist but may contain observations, hypotheses, and proposals |
| `confirmed` | active intent is authority-confirmed, but consistency or coverage may remain incomplete |
| `reviewed` | structure, traceability, conflicts, and placeholders were reviewed |
| `build_ready` | reviewed package plus final product-authority handoff approval |

Never skip directly from source collection to `build_ready`.

## Gate 1 — Governance

Pass when:

- target baseline and target version are declared;
- product boundary and release boundary are confirmed;
- accountable authorities are assigned for every required decision domain;
- delegations are explicit and bounded;
- evidence sources are indexed;
- decision, question, contradiction, and structure/lens coverage ledgers are active.

## Gate 2 — Structural coverage

Pass when all thirteen canonical structures exist and every required coverage lens is:

- represented;
- confirmed not applicable; or
- confirmed out of scope.

The existence of a file does not satisfy the gate. The file must contain the in-scope target detail.

## Gate 3 — Lifecycle journey closure

Pass when:

- every in-scope actor has a journey coverage record;
- every active journey has its required metadata, authority, decision, version,
  status, and intent status;
- each phase and action has a local stable ID;
- each action has an actor-action lane and a product-response lane;
- failure, pause/resume, abandonment, exit, and recovery each have a covered
  disposition or a confirmed exclusion decision;
- each complex transition links a detailed FLOW-*;
- each journey source is editable Markdown with a fenced mermaid block or a
  Markdown lifecycle table;
- qualified trace edges use valid source_part_id values;
- all linked detailed artifacts are current and confirmed;
- no open journey question, assumption, contradiction, or stale dependent
  remains.

Record this result as the journey_closure readiness gate. A journey does not
replace detailed flows, screens, rules, state machines, contracts, sequences,
quality constraints, or acceptance scenarios.

## Gate 4 — Capability traceability

For every in-scope `CAP-*`:

- actors are linked;
- applicable domain concepts are linked;
- applicable user flows/screens/components are linked;
- behavior rules/state machines/decision tables are linked;
- data models are linked where data is read or written;
- architecture responsibility is linked;
- contracts are linked for every boundary;
- a sequence is linked where ordering or coordination matters;
- quality constraints are linked;
- acceptance scenarios are linked.

A capability may waive a dimension only through a confirmed exception decision.

## Gate 5 — Behavioral closure

Pass when:

- every state and transition has a trigger, guard, result, and failure behavior;
- every transition that crosses physical services identifies its initiator,
  durable authority, executor, observers, and failure or recovery path;
- every action has permission and account-state behavior;
- every user-visible surface has applicable loading, empty, success, error, partial, unavailable, and recovery states;
- time, ordering, duplicate, idempotency, retry, concurrency, cancellation, and compensation semantics are explicit where relevant;
- data creation, mutation, retention, export, archival, and deletion are explicit;
- external integrations have timeout, rate-limit, failure, retry, and fallback behavior;
- admin/support/operations paths are covered where needed;
- no behavior-affecting prose is unlinked to a structural artifact.

## Gate 6 — Technical closure

Pass when:

- every physical runtime or service has one clear responsibility boundary,
  owned state, confirmed provider or runtime, and labelled connections;
- every cross-boundary exchange has a contract;
- deployment environments, configuration, secrets, migrations, rollback, backups, and observability are defined;
- security and privacy controls map to data and trust boundaries;
- measurable quality constraints are feasible or explicitly accepted as risks;
- implementation choices outside the package are covered by bounded discretion grants.

## Gate 7 — Verification closure

Pass when:

- every capability has success, invalid-input, permission, failure, and recovery scenarios as applicable;
- every rule and state transition has acceptance coverage;
- every quality constraint has a verification method;
- acceptance results are observable and non-ambiguous;
- representative test data and edge cases exist where outcomes depend on values or ordering.

## Gate 8 — Consistency

Pass when:

- all stable IDs are unique and resolvable;
- all traceability edges resolve;
- no active artifact points to a superseded or stale artifact;
- the runtime stack, state-transition allocation, sequences, data and boundary
  records, registries, and acceptance scenarios agree;
- no unresolved contradiction remains;
- every canonical structure and coverage lens is marked covered, confirmed not applicable, or confirmed out of scope;
- no `TBD`, `TODO`, `UNSET`, `UNKNOWN`, placeholder, or implicit default remains in active intent;
- a consistency review finds no unresolved or conflicting active intent.

## Gate 9 — Handoff approval

Pass when the accountable release/product authority confirms:

- the package version is the intended target;
- the listed exclusions and discretion grants are accepted;
- no additional clarification should be needed for implementation;
- any known risk is explicitly accepted and linked to a decision.

`handoff/readiness.yaml` records each named gate, including `journey_closure`,
with `passed` and `evidence_refs`. It also records the final approval decision.

## Handoff output

A complete handoff contains:

1. the Product Intent Package directory;
2. completed readiness record;
3. unresolved-question count of zero;
4. stale-artifact count of zero;
5. contradiction count of zero;
6. explicit build scope and target version;
7. explicit discretion grants;
8. final authority approval decision.

If any count is nonzero, output a blocked handoff report instead of pretending the package is complete.

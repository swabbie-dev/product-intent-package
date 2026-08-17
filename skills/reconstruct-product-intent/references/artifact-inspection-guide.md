# Artifact Inspection Guide

## Source-to-structure map

| Source | Inspect for | Confirm elsewhere |
|---|---|---|
| routes/navigation | reachable surfaces and topology | hidden states, intended IA, removed/legacy paths |
| UI components | visual patterns, variants, event handlers | approved design system, missing states, responsive intent |
| state stores/domain code | entities, states, transitions, invariants | business intent, unreachable branches, future target |
| validation code | input constraints and error handling | user-facing rule, localization, exact copy |
| permissions/auth | role checks and trust boundaries | complete authorization matrix and policy rationale |
| database schema/migrations | physical model, constraints, historical changes | domain model, retention, deletion, privacy intent |
| APIs/events | boundary shapes and actual exchanges | target contract, versioning, failure/retry semantics |
| queues/jobs | async sequences and timing | ordering, idempotency, recovery, SLOs |
| tests | asserted examples and regressions | complete coverage and current authority |
| configs/feature flags | environment variance and latent behavior | intended release state and ownership |
| CI/CD/IaC | deployment topology and checks | operational target, rollback, DR, support ownership |
| logs/metrics/alerts | observable behavior and incidents | desired SLOs, business meaning, missing telemetry |
| mockups/design files | intended visual/interaction states | final approval, backend behavior, all branches |
| tickets/docs/roadmaps | stated requirements and rationale | current validity, conflict resolution, release target |
| support/research | real pain and edge cases | solution choice and priority |

For journey candidates, inspect actor actions, product responses, state/data/event
effects, exceptions, hand-offs, recurrence, and terminal conditions. Register
each claim as evidence first. A journey diagram, funnel, screenshot, or
rendered image cannot prove lifecycle intent.

## Runtime capture checklist

For each `JOURNEY-*` and `FLOW-*` candidate, capture as evidence where available:

- actor, role, account state, entitlement, and environment;
- initial data state;
- actions and inputs;
- screen transitions and all visible states;
- network/API exchanges;
- data mutations;
- emitted events/notifications;
- background operations;
- failures, retries, timeouts, cancellation, undo, and recovery;
- final state and side effects;
- lifecycle phase, actor action, product response, failure, pause/resume,
  abandonment, exit, and recovery disposition;
- version/commit/feature flags.

## Static-analysis cautions

Do not assume:

- an endpoint is reachable because it exists;
- an enum value is a valid product state because it is declared;
- a test name is accurate;
- a database column is user-visible;
- a component variant is approved or used;
- a feature flag represents future intent rather than abandoned code;
- comments are current;
- a missing error branch means the intended behavior is to crash;
- repeated implementation patterns are product requirements.
- a marketing funnel is a product lifecycle;
- a diagram proves actor emotion, motivation, or desired intent;
- one actor lane represents materially different roles.

## Evidence confidence

Use confidence only for the evidence claim, never for intent:

- `high`: directly observed or deterministically derived from the inspected version;
- `medium`: strongly supported but dependent on reachability/configuration/context;
- `low`: heuristic interpretation requiring confirmation.

Even high-confidence evidence remains non-canonical until the accountable authority confirms it as target intent.

For reconstruction, keep observed, inferred, proposed, and confirmed journey
intent separate. When a journey phase changes, mark the parent journey and all
linked detailed artifacts stale until review and confirmation.

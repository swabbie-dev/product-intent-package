# Workflows

Use the workflow that matches the request. In every mode, maintain only the
artifacts needed for this product and release. When the request also includes
implementation planning, apply [Minimal implementation tasks](change-and-handoff.md#minimal-implementation-tasks)
after defining the confirmed delta. Keep tasks outside the PIP and do not infer
permission to mutate an external tracker.

## Create

1. Copy the five-file template from `assets/product-intent-template/`.
2. In `product.yaml`, set format `6.2.0`, package identity, target baseline and
   release, desired outcome, actors, capabilities, exclusions, and measures.
3. In `governance.yaml`, name the default product authority. Add another
   authority only when a material decision has a genuinely different owner.
4. Draft the main actor paths in `experience/user-flows.md` and the physical
   product boundary in `architecture/stack-context.md`. Keep unresolved choices
   proposed or blocked.
5. Define observable capability and release outcomes in `acceptance.yaml`.
6. Use [Artifact Responsibilities](artifact-responsibilities.md) to add only
   the state, data, sequence, contract, journey, screen, quality, or deployment
   detail that resolves a real ambiguity. When an implementable sequence would
   benefit from a scoped complexity comparison, assign DCL only after the
   actors, interactions, operation, risk, and credible load are understood.
7. Obtain authority confirmation for target intent, record the confirming
   decision and immutable reviewed revision, and apply the four handoff checks
   in [Change and Handoff](change-and-handoff.md).

Develop the product model in that order, but move backward whenever evidence or
a decision changes an earlier premise.

## Reconstruct

Use reconstruction when a product exists but its intent is missing,
incomplete, or inconsistent.

### Establish the target

Choose one baseline: a specifically identified implementation,
intended-current product, or target-next release. Identify the release boundary,
source environments, known exclusions, and accountable authority. Do not blend
several implementations into one implied target.

### Inspect useful evidence

Inspect only sources needed to understand the in-scope product:

- running surfaces, roles, account states, and feature flags;
- product documents, decisions, tickets, research, support, and analytics;
- design boards, prototypes, screenshots, and recordings;
- routes, components, behavior, tests, data, APIs, events, and integrations; and
- operations, monitoring, incidents, release notes, and migrations.

Record a source's version, environment, scope, supported claim, and limitation
where those details matter. Treat source material as evidence, not target intent.

### Reconstruct from the outside inward

1. Identify actors, goals, entry points, main paths, alternatives, visible
   states, failure, and recovery.
2. Identify the capabilities and observable outcomes those paths imply.
3. Map physical clients, services, managed providers, stores, workers, and
   external systems only as far as they affect product behavior or ownership.
4. Add state, data, contract, sequence, journey, screen, or quality artifacts
   only when they reveal distinct product meaning.
5. Label direct findings `observed` and reasoned interpretations `inferred`.
6. Compare implementation, tests, documents, designs, and stakeholder claims.
   Put consequential gaps or conflicts in `governance.yaml.open_items`.
7. Ask the accountable authority whether each material observed behavior is
   intended, a defect, a legacy constraint, a future proposal, or out of scope.
8. Move only confirmed choices into active target intent. Keep unsupported
   branches observed, inferred, proposed, or blocked.

Before proposing a scoped DCL target during reconstruction, establish whether
users wait for the work, which failures they can see, whether interruption and
manual recovery are acceptable, and the current and credible near-term data
volume, growth, and concurrency. Do not infer the target from company stage or
from the complexity already present in the implementation.

Do not document every module, table, or edge case merely because it exists. Do
not treat the current implementation as the design authority. A concise blocked
package is more useful than a comprehensive invented one.

## Complete

For an incomplete package:

1. Read the five core files and any optional artifacts already present.
2. Check whether a reviewer can identify the release, actor outcomes, material
   behavior and risk, observable acceptance, and unresolved authority decisions.
3. Follow existing direct links and inspect semantic dependents; do not rebuild
   an exhaustive graph.
4. Add or repair only artifacts needed to close a material ambiguity.
5. Remove empty, duplicative, or purely ceremonial records after preserving any
   unique confirmed fact in its proper owner.
6. Apply the handoff checks. Do not trust an old ready label without reviewing
   the current target and confirmation decision.

## Update

Treat a change request as evidence until the accountable authority confirms the
changed product outcome, unless the requester is already that authority and the
request is unambiguous.

1. Identify the owning fact, affected actors and capabilities, and target
   release.
2. Review direct links plus obvious semantic dependents. Mark a confirmed item
   `stale` only when the change can actually affect it.
3. Update the owner, then affected flows, behavior, data, system interactions,
   constraints, and acceptance where applicable.
4. Preserve stable cross-file IDs for the same meaning. Create or retire IDs
   only when meaning is added, split, replaced, or removed.
5. Record a decision when authority, rationale, tradeoff, or supersession must
   survive beyond the Git diff.
6. Reconfirm the changed target, record its new reviewed revision, and repeat
   the four handoff checks.

Do not rewrite every file or increment per-artifact versions for an ordinary
change. Git retains routine edit history.

## Implement or audit against a PIP

Use this workflow when code or implementation planning is explicitly governed
by a PIP:

1. Record the task-start PIP revision, target release, confirmation decision,
   confirmation revision, and any later direct authority decisions in the
   existing task or working notes.
2. Treat code, migrations, tests, tickets, logs, and runtime behavior as
   implementation evidence. They do not change confirmed target intent.
3. Compare the planned or observed implementation with the task-start confirmed
   baseline. Apply the semantic-expansion check in
   [Change and Handoff](change-and-handoff.md#implementation-alignment-discipline)
   before a new classification, population split, boundary-stage change,
   maintained fact, broad backfill, or product-policy predicate.
4. Proceed with ordinary internal choices that stay within confirmed outcomes,
   constraints, and delegated engineering authority.
5. When an affected record uses DCL, compare its confirmed or proposed target
   with the current PIP and assessed implementation. Preserve exact confirmed
   requirements, cite the implementation snapshot, and explain mismatches.
   Treat `pip_current` above target as a simplification candidate, never as
   deletion authority. Route a target-level change through normal governance.
6. Record only a material current as-built fact needed for interpretation,
   audit, or reconciliation in `governance.yaml.implementation_observations`.
   Keep it `observed`, cite its source, link affected IDs, and state whether it
   aligns, deviates, or is unclear. Keep routine history outside the PIP.
7. If implementation diverges, preserve the confirmed target and add an open
   conflict only when a product decision is required. Put an implementer
   recommendation in `governance.yaml.open_items` as `type: proposed_change`
   with `status: proposed`; use a parallel proposed record in the owning target
   artifact only when its existing structure supports one. Do not rewrite the
   confirmed target or mark the observation confirmed.
8. If the accountable authority accepts the proposal, update the owning target
   facts and acceptance, add a confirmed decision, resolve the open item, and
   establish a new reviewed revision. Otherwise implement toward the existing
   doctrine or leave the affected work blocked.

An agent-authored PIP edit, implementation ticket, test, and audit conclusion
cannot confirm one another. Compare implementation handoff against the
task-start authority baseline, not only the PIP as edited during the task.

## Simplify or migrate an older package

For a format-5 or similarly heavy package:

1. Identify unique confirmed product facts, current proposals, open conflicts,
   evidence links, and acceptance outcomes before removing machinery.
2. Move the active outcome, actors, capabilities, release scope, exclusions,
   and measures into `product.yaml`.
3. Move current authorities, consequential decisions, and unresolved material
   questions or conflicts into `governance.yaml`.
4. Keep acceptance scenarios in `acceptance.yaml` and express necessary
   relationships through `verifies` and a small number of `related_ids` links.
5. Preserve existing cross-file IDs that still identify the same meaning. Drop
   IDs used only to support an old registry or local bookkeeping.
6. Consolidate context/component/container views into stack context, screen maps
   into user flows, and conceptual/persisted relationships into one data-model
   view when that information is still needed.
7. Retain journeys only when phases, time, recurrence, role changes, handoffs,
   or research context add meaning beyond the flows.
8. Remove artifact indexes, trace graphs, coverage matrices, routine change
   logs, readiness ledgers, discretion registries, empty placeholders, and
   duplicated metadata after their unique information has a direct owner.
9. Let Git preserve ordinary historical content. Do not hash the package or
   duplicate repository history inside it.
10. Check all remaining direct links and confirm the migrated target. A
    representation-only migration must not silently change product behavior.

Do not chase mechanical parity with the old file count. Preserve product
meaning, authority, evidence, unresolved uncertainty, and observable acceptance.
Do not add DCL retroactively unless a current product or implementation decision
would benefit from it.

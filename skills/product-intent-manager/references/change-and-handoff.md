# Change and Handoff

## Change discipline

For a material product-intent change:

1. Identify the authoritative fact and the target release.
2. Confirm the changed observable outcome with the accountable authority when
   the request itself is not already an authoritative, unambiguous decision.
3. Follow direct links and review obvious semantic dependents. Mark only items
   that may actually be affected as `stale`.
4. Update the owner first, then affected flows, optional detail, and acceptance.
5. Resolve or expose any contradiction introduced by the change.
6. Reconfirm the affected target scope and update the package status.

Preserve a stable cross-file ID when the meaning is unchanged. If meaning is
split or replaced, retain enough decision context to explain the relationship.
Do not maintain a global dependency graph, per-artifact version counter, or
package hash to automate this judgment.

Use Git for ordinary history. Add a `DEC-*` record only when authority,
rationale, a consequential tradeoff, or supersession must remain visible in the
active package. Do not duplicate every diff in a change log.

## Implementation alignment discipline

At the start of PIP-governed implementation or audit, note in the existing task
or working context:

- the task-start PIP Git revision and target release;
- `confirmation_decision_id` and `confirmation_revision`, when present; and
- any later direct authority statements that change the confirmed baseline.

Do not create another ledger. Same-task PIP, ticket, audit, test, diagram, or
code changes do not become independent authority merely because they agree.

Before implementation handoff or push, compare product-significant schema,
migration, query, policy, and behavior changes with that task-start confirmed
baseline, not only with PIP text edited on the working branch. Apply the
semantic-expansion boundary in
[Authority and Evidence](authority-and-evidence.md#inference-and-proposal). A
semantic delta must map to an independently confirmed decision or remain
proposed or blocked. Ordinary implementation choices inside confirmed behavior
and material constraints do not need this review.

When current implementation materially helps future interpretation, use the
sparse observation pattern in
[Product Intent Package Standard](product-intent-package-standard.md#product-doctrine-and-implementation-observations)
and leave the confirmed target intact. A divergence requires an open conflict
only when a product decision is needed; divergent code does not by itself make
a clear target PIP unready. Routine history stays in Git or tasks.

## Staleness

`stale` means a prior item should not be relied on until its relationship to a
changed dependency is reviewed. It does not mean every linked artifact must be
rewritten. After review:

- update and reconfirm the item if its meaning changed;
- restore its prior active status if it remains correct; or
- remove or replace it if it no longer belongs in the target.

Keep stale items visible only while they affect current work. Git preserves
superseded ordinary content.

When a stale or superseded artifact remains in the active package because its
history still matters, link it directly to its active successor. Otherwise
remove it from the active package and rely on Git history.

## Proportional package checks

After a change:

- safely parse changed YAML and preserve unique keys without aliases, anchors,
  or custom tags;
- resolve direct IDs and local links touched by the change;
- render each changed Mermaid diagram, and render the full diagram inventory
  only when shared styling or another renderer-sensitive convention changes;
- verify changed source and intent-status statements; and
- when the package is tracked in Git, run `git diff --check`.

Use existing project tools when available. If a renderer is unavailable, report
that visual verification was skipped. These are documentation checks, not a
reason to add Python, package hashes, snapshot tests, a new dependency, or a
full-package validator.

## Minimal implementation tasks

The confirmed PIP describes the intended product, while the project's existing
task tracker or implementation notes describe the shortest practical route from
the current codebase to that product. Keep task state, assignment, sequencing,
and working notes outside the PIP. Link tasks to the target release and relevant
PIP IDs rather than copying diagrams, acceptance scenarios, or product rules.

Create or change tasks in an external system only when authorized. Otherwise,
return a draft task set. Do not introduce a new tracker, PIP task file, task
registry, or parallel implementation plan when the project already has a place
for this work.

### Write the smallest coherent task set

A task should contain no more than the implementer needs to act without product
guesswork:

- the confirmed outcome and relevant PIP links;
- the verified code or design owner to reuse or modify when that anchor matters;
- only essential ordering or dependency information;
- an observable done condition; and
- the smallest relevant verification.

Keep one product outcome together even when it touches several files or layers.
Split only for independent ownership, dependency order, material risk, release
scope, or work that can genuinely ship or be reviewed separately. Do not split
by artifact, component, file, acceptance scenario, or checklist item merely to
make progress easier to count. Do not turn proposed or blocked intent into a
build commitment.

When writing or reviewing each task, ask:

1. Does every instruction directly move the codebase toward confirmed PIP
   intent?
2. Is the task more detailed than necessary, or can instructions or tasks be
   removed or merged?
3. Does it modify or reuse existing code, tests, tools, and project process
   wherever practical?
4. Is every requested test, gate, proof, report, or review necessary to protect
   a core outcome or dangerous edge case?

Delete ceremony that does not survive those questions. A task can link to the
owning sequence, mockup, state machine, user flow, or acceptance scenario; it
does not need to restate their content. If implementation planning exposes a
product decision or changes the desired end-state, route that change back to
the PIP and accountable authority instead of settling it only in the task.

### Verify in proportion to consequence

Implementation verification should cover:

- the core intended path and observable done condition;
- material failure or recovery behavior explicitly required by the PIP; and
- dangerous edge cases relevant to the changed area.

Treat an edge case as dangerous when a plausible failure could cause an
authorization, security, or privacy breach; incorrect money movement or
billing; data loss or corruption; an unsafe schema or migration result; a
destructive or irreversible side effect; or another comparably high-impact
product or operational harm. Use existing focused checks where practical. Add
or update a test when it efficiently protects one of these outcomes, but do not
enumerate every hypothetical case, chase blanket coverage, or require new test
harnesses, approval gates, proof documents, screenshots, or reports unless a
specific risk or project requirement makes one necessary.

## Four handoff checks

### 1. Scope and authority

Confirm that:

- the target baseline, release boundary, outcome, actors, capabilities,
  exclusions, and measures are understandable and mutually consistent;
- target intent is confirmed by the accountable authority, with a direct
  confirmation decision and reviewed revision for a newly confirmed or
  materially reconfirmed package; and
- every unresolved question or conflict that could change the release is either
  resolved or clearly blocks handoff.

Do not require formal disposition of irrelevant possibilities.

### 2. Material behavior and risk

Confirm that the package explains the user-visible and operational behavior
needed for this release, including applicable failure and recovery outcomes,
permissions, meaningful state changes, data relationships, system ownership,
external boundaries, and material quality, security, privacy, compliance, or
operational constraints.

Use optional artifacts where they genuinely clarify these matters. Do not fail
the check because an unnecessary artifact type is absent.

For an existing-product or design-led handoff, also confirm that:

- each consequential sequence step names any verified existing code anchor and
  says whether to `reuse unchanged` or `modify existing`, while any `new` code
  has a stated reason;
- each consequential sequence input states where its value originates; and
- each user-flow surface or state governed by a confirmed mockup links to that
  exact target and companion example or export code when available, while any
  intended deviation has accountable approval.

When the PIP explicitly constrains an index or concurrency mechanism, confirm
that the index uses matching attribute badges and an index compartment to show
its affected columns, status, confirmed intent, and product purpose. Confirm
that a concurrency restriction traces to its named invariant or capacity bound
and is no broader or longer than that constraint requires. Leave unconfirmed
physical choices to engineering.

An index or constraint may support an owning confirmed rule but cannot establish
that rule. Before treating a persisted classification or policy predicate as
confirmed, verify that the owning target fact defines its meaning, affected
population, owner and update lifecycle, and consumers.

When the PIP explicitly constrains database connection use, confirm that it
considers aggregate fan-out across replicas and workers, permits necessary
parallel and session-bound work, and does not assert an unsupported numeric
limit.

Do not require a concurrency mechanism merely because multiple processes might
touch the same database. Preserve parallel work on modest infrastructure unless
a confirmed correctness invariant or material capacity bound establishes the
need to coordinate it.

### 3. Acceptance and engineering discretion

Confirm that `acceptance.yaml` contains observable scenarios for the in-scope
capabilities and material constraints. Scenarios should be specific enough to
recognize success or failure without dictating internal construction.

For an authority-confirmed mockup, acceptance names the required visible states
and interactions and references the exact mockup for fidelity. Do not duplicate
every visual detail into YAML merely to make it testable.

Any unspecified implementation choice remains with engineering by default when
it stays within confirmed behavior and material constraints. Seek another
decision only when a plausible choice could change those outcomes or bounds.

Engineering discretion does not permit a silent parallel replacement for a
confirmed reuse or modification anchor, or an unapproved change to a confirmed
mockup's views, components, states, or interactions. Route a material conflict
to the accountable technical, product, or design authority.

### 4. Consistency and approval

Confirm that:

- remaining direct links resolve and linked artifacts do not contradict their
  owners;
- no `blocked` or `stale` item remains in the approved release scope;
- observed, inferred, and proposed material is not presented as confirmed
  target intent; and
- implementation observations are visibly `observed`, source-backed, sparse,
  and separate from target doctrine; and
- the accountable product authority, or an authority with explicit delegated
  product scope, approves the package target.

Record readiness only in `product.yaml`: set `status: build_ready` and set
`confirmation_decision_id` to the approving decision in `governance.yaml` and
`confirmation_revision` to the immutable target-intent revision that decision
reviewed. The reviewed revision normally precedes the signoff metadata commit.
Do not create a separate readiness file or gate ledger. Legacy format-6
packages may add the revision at their next material reconfirmation.

## Handoff result

Report two independent results; do not make implementation behavior product
authority by collapsing them:

- **PIP target authority and readiness:** state the package status and target
  release. For `build_ready`, name the confirmation decision and reviewed
  revision. For `blocked`, name the smallest unresolved questions, their
  authorities, affected outcomes or IDs, and what can proceed independently.
- **Implementation alignment:** state `aligns`, `deviates`, or `unclear`, then
  name only the material observations and remaining engineering discretion. A
  build-ready target may coexist with deviating implementation.

A package may be useful before it is ready. Do not hide uncertainty to produce
a ready label, and do not delay a ready package because non-observable
engineering decisions remain open.

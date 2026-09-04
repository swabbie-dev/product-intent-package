# PIP Use and Alignment Checks

These are instructions for people and agents using a PIP. They are not PIP
content. Never create package status, readiness, signature, approval, gate,
handoff, checklist, or review-result fields or files because of these checks.

## Change discipline

For a material product-intent change:

1. Identify the owning fact and release, then verify the requester's identity
   and current editing authority from `governance.yaml` or unambiguous project
   guidance.
2. Follow direct links and review obvious semantic dependents before deciding
   whether the complete change fits that authority.
3. If the new end state is not already an unambiguous authorized decision, or
   any required dependent edit falls outside a scoped editor's access, create
   one complete isolated PIP fork rather than editing the canonical package.
   Never apply only an in-scope fragment that leaves canonical intent
   contradictory, unstable, or incomplete.
4. When authority covers the complete change, update the owner first, then
   affected flows, behavior, data, architecture,
   sequences, constraints, and acceptance.
5. Write affected content as present-tense facts or timeless requirements for
   the resulting product, not instructions to change it. Refresh `Current
   rationale` with only the active reasons for that design.
6. Resolve contradictions outside the package, then adopt one coherent end
   state through an editor whose authority covers the complete change and the
   team's normal Git process. Do not create a per-change signoff or approval
   record; Git owns commit history.

Preserve a stable cross-file ID when meaning is unchanged. Do not maintain a
global dependency graph, per-artifact version counter, package hash, change log,
or product history inside the PIP.

## Implementation alignment

At the start of PIP-governed implementation or audit, note the canonical PIP Git
revision and release in the existing task or working context. Compare product-
significant behavior, design, schema, migration, query, policy, and data changes
with that baseline and later direct instructions from a verified authority whose
scope covers the change.

For an audit, a ticket may guide which implementation area, code, and PIP
records to inspect. It is not the conformance target. Derive expected behavior,
acceptance, constraints, diagrams, data rules, and design targets from the
canonical PIP owners. Follow direct links and obvious semantic dependents needed
to assess the requested scope. A completed ticket, checked box, passing test, or
faithful-looking paraphrase does not establish PIP alignment.

Implementation findings stay in the task, audit, or code review. Do not add an
as-built lane, implementation observation, deviation status, or implementation
DCL to the PIP. If the implementation is wrong, fix it toward the PIP. If the
team wants different product intent, create a coherent PIP fork and route that
product change separately. Report ticket-to-PIP drift separately from
implementation-to-PIP drift so neither is mistaken for product authority.

Apply the semantic-expansion boundary in
[Authority and Evidence](authority-and-evidence.md#semantic-expansion-boundary)
before persisting a new classification, splitting a population, moving a rule
between processing stages, adding maintained derived state or a broad backfill,
or encoding product policy in a database predicate.

## Minimal implementation tasks

This section defines the boundary with companion tasks, not a task-management
system or required workflow. Use the team's existing tracker or working notes.

The PIP describes the intended product. An implementation ticket in Linear,
Notion, ClickUp, GitHub, or another task system describes only the shortest
practical route from the codebase to that product. It is an execution overlay,
not a second specification. Keep tasks, assignment, order, progress, and
verification outside the PIP. Identify the canonical PIP release or revision
and link directly to the relevant records or files.

Do not copy, summarize, reinterpret, or rewrite product behavior, acceptance,
constraints, diagram logic, data rules, or design targets into a ticket. Even a
faithful paraphrase creates another version that can drift or be mistaken for
authority. A task may narrow implementation scope but cannot revise the linked
PIP. When the task and PIP conflict, follow the PIP and correct or clarify the
task. When the PIP lacks needed product meaning, resolve that gap through the
PIP authority process rather than making the ticket authoritative.

Create or mutate an external task only when authorized. Otherwise return a
draft. Do not introduce a PIP task file, task registry, or parallel tracker.

A task should contain no more than the implementer needs to act without product
guesswork:

- a concise implementation objective and direct PIP links or record IDs;
- the execution boundary: what code, schema, configuration, or surfaces to
  touch and what adjacent areas not to touch;
- reuse/modify directions for verified code or design owners when they matter;
- only essential ordering or dependency information;
- codebase-specific tips, known hazards, assumptions to verify, or blockers;
- assignment, progress, and links to implementation evidence when useful; and
- the smallest relevant verification or completion evidence.

State completion as alignment with the linked PIP plus task-specific evidence.
Do not duplicate PIP acceptance as a ticket checklist.

Keep one product outcome together even when it touches several files or layers.
Split only for independent ownership, dependency order, material risk, release
scope, or work that can genuinely ship or be reviewed separately. Do not split
by file, component, layer, diagram, scenario, or checklist item merely to make
progress easier to count.

For each task, ask:

1. Does every instruction directly align the codebase with the PIP?
2. Does it link to product truth instead of restating or interpreting it?
3. Can any instruction or task be removed or merged?
4. Does it reuse existing code, tests, tools, and project process where useful?
5. Does every requested test, gate, proof, report, or review protect a core
   outcome or dangerous edge case?

Remove ceremony that does not survive those questions.

### Verify in proportion to consequence

Implementation verification should cover the core path and observable done
condition, material failure or recovery behavior required by the PIP, and
dangerous edge cases relevant to the change.

An edge case is dangerous when a plausible failure could cause an authorization,
security, or privacy breach; incorrect money movement; data loss or corruption;
an unsafe schema or migration result; a destructive or irreversible side
effect; or comparable product or operational harm. Prefer existing focused
checks. Do not enumerate every hypothetical case, chase blanket coverage, or
require new test harnesses, proof documents, screenshots, gates, or reports
without a specific risk or project requirement.

Before expanding design, implementation, or verification for a rare or complex
edge case the PIP does not resolve, ask the product manager, originator, or
other human product authority whether current intent is automatic handling,
safe manual review or recovery, visible failure or deferral, or exclusion from
the release. Do not infer the answer from DCL. Record the adopted behavior in
its owning PIP artifact before adding it to an implementation task. A manual
resolution path must still prevent dangerous effects from occurring before
review.

For a manual fallback, first verify that a responsible admin or operator will
actually become aware of the incident through a monitored path and receive
enough context to identify and investigate it. Do not require bespoke admin
screens, queues, or action controls unless the intended response cannot be
performed safely with existing tools or real frequency, urgency, or volume
justifies them. Visibility is the default requirement; a full control surface
is not.

## Four lightweight checks

Run these as review questions. Do not store their answers in the PIP.

### 1. Coherent current intent

Confirm that the release, outcome, boundary, actors, capabilities, exclusions,
measures, and acceptance are understandable and consistent. The canonical PIP
must describe one current end state, without alternatives, statuses,
implementation findings, or historical narration.

Read affected YAML, diagram labels, supporting notes, and acceptance as a
description of the intended product. Would they still make sense without
knowing the previous design or pending work? Apply the
[end-state wording guidance](product-intent-package-standard.md#write-the-end-state-not-the-change):
keep runtime behavior and intended owners, move construction steps and progress
outside the PIP, and do not treat present-tense intent as evidence of delivery.

If a material product question remains, resolve it outside the package. Keep the
canonical PIP unchanged and use an isolated PIP fork for a concrete alternative.

### 2. Enough product and process meaning

Confirm that the package explains applicable:

- actor-visible surfaces, states, paths, failure, and recovery;
- lifecycle states and the high-level interaction of consequential processes;
- detailed process ordering, input provenance, retry, fallback, and recovery in
  sequences;
- physical systems, responsibility, owned state, deployment, and external
  boundaries;
- product-significant data relationships, constraints, indexes, and concurrency;
  and
- material quality, security, privacy, compatibility, operational, and cost
  bounds.

Use optional artifacts only where they add distinct meaning. An absent optional
artifact is not a failure.

For an existing-product or design-led implementation, also check that:

- sequences name intended code owners and their runtime responsibilities,
  preserving suitable existing owners without construction-task labels;
- consequential inputs state their source;
- consequential database steps name each physical table or view and operation,
  reference the canonical index badge when applicable, or show exact key fields
  when no canonical index applies;
- user-flow surface boundaries identify what needs mockups;
- exact linked mockups and compatible example code are followed; and
- every diagram's current rationale succinctly covers the active reasons for
  its design without recounting history.

For product-significant database design, check that:

- persisted columns that determine product behavior appear individually with
  exact physical names, types, and material constraints rather than synthetic
  grouped rows, while abbreviated cross-diagram references are clearly marked;
- each physical index has exactly one badge and one complete `INDEXES`
  compartment entry; indexes are never grouped under one badge or abbreviated
  as `same key`, and every attribute badge matches its key order, predicate,
  expression, or included-column role without a redundant same-index `·where`;
- routine primary-key indexes remain `PK` entity facts unless their particular
  physical definition has an independently product-significant purpose;
- each index states its product or process reason;
- an index or predicate supports an independently stated product rule rather
  than inventing a classification;
- any explicit lock or serialization protects a named invariant, is no broader
  or longer than needed, and cannot be replaced by a simpler narrow mechanism;
- persisted lease fields use matching ERD coordination badges and a
  `COORDINATION` compartment, while runtime acquisition, renewal, expiry,
  fencing, release, and recovery stay in the owning sequence;
- every index or coordination badge sits on the exact physical column and type,
  never a grouped field or abbreviated reference projection;
- sequence access annotations agree with the linked ERD table names, index
  badges, and key fields without duplicating full index definitions or promising
  query-planner behavior;
- a coordination overlay is present only when multiple contenders or mechanisms
  need a contention map, and it agrees with the linked sequence and data model;
- connection design considers aggregate fan-out and combines process-local
  clients or pools where that preserves effective concurrency and session
  needs; and
- the design does not require oversized infrastructure to compensate for
  avoidable contention or connection amplification.

When DCL is used, check that the product default and any narrow override are
based on current users, interactions, wait path, failure consequences, recovery,
credible load, and material risk. Do not require DCL on every record or treat a
number as permission to add or remove mechanisms. Confirm that rare or complex
edge-case handling reflects an explicit automatic, manual, visible fallback, or
excluded product choice rather than an assumption derived from DCL. When a
manual fallback exists, confirm that it provides monitored admin awareness
without inventing controls the actual response does not need.

### 3. Observable acceptance and engineering discretion

Confirm that every in-scope capability has observable acceptance. Inline
acceptance is preferred; a separate `acceptance.yaml` is warranted only when
scenario detail improves clarity. Acceptance should recognize success and
material failure without dictating ordinary construction.

An exact current mockup target must cover its required visible states and
interactions. Do not duplicate every visual detail into YAML.

Unspecified internals remain with engineering when choices stay inside PIP
behavior and constraints. This discretion does not permit a parallel replacement
for a stated code owner or a silent change to current mockups, views,
components, states, or interactions.

### 4. Consistency, format, and implementation alignment

Confirm that direct links resolve, linked artifacts do not contradict their
owners, YAML parses with unique keys, changed Mermaid renders when practical,
and `git diff --check` is clean when Git is used.

Separately compare implementation with the PIP when implementation is in scope.
Report `aligns`, `deviates`, or `unclear` in the task or audit response and name
only material differences. Use a ticket to guide audit scope, never as the
expected product. Do not persist that result in the package, and do not change
the PIP to make a divergent ticket or implementation appear compliant.

Use existing tools and proportional manual checks. A missing renderer should be
reported, not solved by adding Python, a package hash, snapshot tests, a new
dependency, or a full-package validator.

## Report

Return a concise human-readable result: what PIP content changed, the release
boundary, optional artifacts added or removed, unresolved product questions
kept outside the PIP, and—when implementation was reviewed—material alignment
findings and minimal follow-up tasks. Do not generate a persistent handoff or
readiness artifact.

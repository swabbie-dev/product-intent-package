# Artifact Responsibilities

## Selection rule

Use the smallest set of artifacts that answers the product questions at hand.
Every artifact must own distinct information. If two artifacts would explain
the same fact, keep the fact in the more appropriate owner and link to it.

The four default files establish product scope, acceptance, the physical system
map, and actor flows. Add the following only when triggered:

| Optional artifact | Add when |
| --- | --- |
| Governance | Several product leaders or delegated authorities need explicit scope, precedence, supersession, or durable cross-team rationale |
| Journey map | Time, phases, recurrence, roles, or handoffs add context that a focused flow cannot show |
| Screen records | Screen-specific content, actions, validation, responsive behavior, or visible states need detail beyond the flow |
| Design records | Repeated visual, content, component, interaction, responsive, or accessibility rules constrain the design handoff |
| Rules or decision table | Several conditions, priorities, permissions, or calculations select an outcome |
| State machine | A product or domain object has meaningful valid states and transitions |
| Data model / ERD | Entity identity, ownership, relationships, or cardinality affect the product |
| Schema detail | Fields or constraints are product-significant or form a shared boundary |
| API, event, or integration contract | A boundary is shared, external, compatibility-sensitive, or product-significant |
| Sequence | Ordered cross-system work, async behavior, or recovery changes an outcome |
| Quality constraints | A measurable performance, reliability, security, privacy, accessibility, compatibility, operations, or cost bound matters |
| Separate deployment view | Environment, region, network, failover, or rollout topology makes stack context hard to read |

Do not create a file merely to record `not applicable`. State a consequential
exclusion in `product.yaml`; otherwise omit the artifact.

## Diagram responsibilities

| View | Question it owns |
| --- | --- |
| Stack context | What physical systems exist, what does each own, and how do they connect? |
| User flow | What does the actor do, see, choose, and experience next? |
| State machine | Which lifecycle states and process-triggered transitions are valid? |
| Data model / ERD | What concepts or persisted entities exist, and how do they relate? |
| Sequence | How does one consequential process execute across physical systems, including material retries and fallbacks? |

These views are enough for ordinary application work. A decision table is a
supporting logic format, not another diagram type. Deployment is usually part
of stack context and becomes separate only under the trigger above. Do not add
component, container, system-context, screen-map, domain-model, or similar
diagrams that repeat one of these views.

Keep diagrams with the same responsibility consolidated by default. When a
consolidated file becomes difficult to read or review, split it into one
ID-named Markdown file per diagram and provide a simple table of contents with
direct links. The table of contents is navigation, not an artifact registry or
trace graph. Do not split files or create diagrams merely to fill ID gaps.

## One fact, one owner

| Information | Owner |
| --- | --- |
| Outcome, actors, capabilities, release boundary, exclusions, measures | `product.yaml` |
| Current product target | Its owning product, flow, behavior, data, architecture, quality, or acceptance artifact |
| Multi-authority scope, precedence, durable rationale, or supersession | Optional `governance.yaml` |
| Material current implementation evidence needed to reconcile the target | A separate local observation beside the owning target; optional governance only for a cross-artifact fact in a multi-authority package |
| Scoped DCL target and current assessments | One optional `dcl` mapping on the owning YAML record, or one local sequence summary when Markdown is the owner |
| Observable proof of product outcomes | `acceptance.yaml` |
| Actor action, navigation, visible outcome, and visible recovery choice | User flow |
| Detailed content and actions for a surface | Screen record, when needed |
| Condition combinations that select an outcome | Rule or decision table |
| Valid states, process-triggered transitions, triggers, and guards | State machine |
| Ordered calls, events, retries, fallbacks, and runtime failure | Sequence |
| Physical responsibility, owned state, provider, and trust boundary | Stack context |
| Entity identity, relationship, and cardinality | Data model / ERD |
| Request, response, event, and error shape | Contract |
| Product-significant field or storage constraint | Schema detail |

## Preserve context with direct links

- A `FLOW-*` action may link to the `SEQ-*` that performs consequential work.
- A sequence uses the same `ARCH-*`, `API-*`, `EVT-*`, and `DATA-*` IDs as the
  physical and boundary records.
- A sequence ends at the same visible `SCREEN-*` outcome or durable `SM-*`
  state used by the flow or state machine.
- A state transition links to a sequence only when ordering or coordination
  matters.
- Acceptance scenarios name the `CAP-*`, `RULE-*`, `SM-*`, or other outcomes
  they verify.

Share an ID and a short label. Do not copy the selecting rule, transition
definition, or runtime messages into every view.

## Target views and implementation observations

Canonical target diagrams and records describe target intent. Reconstruction
may retain a separately labeled observed view, but do not redraw a target view
to match an unapproved implementation. When a material as-built fact needs
local context, add a visibly separate callout labeled `Implementation
observation — observed, not product authority` with its evidence source,
affected IDs, and whether it aligns, deviates, or is unclear relative to the
confirmed target. Keep routine or superseded history in Git or tasks.

Keep an implementation observation beside its owning target by default. It is
a sparse evidence lane, not an implementation registry or change log. Keep a
proposed doctrine change visibly parallel to the current owner when that
artifact supports it, or in the existing task system. A package that already
needs optional multi-authority governance may use its
`implementation_observations` or `open_items` lists for material cross-artifact
facts or proposals that several leaders must coordinate.

An optional local `dcl` mapping deliberately places a scoped target beside
`pip_current` and `implementation_current` assessments for comparison. Only the
target is doctrine, and it follows normal proposal and adoption rules. The
two current levels and any `gap_note` are inferred analysis even when their
basis cites observed PIP or implementation facts. Do not let their proximity to
a confirmed target or build-ready package give them product authority.

## User flows

A user flow owns observable experience. Include the actor goal and entry point,
actions and choices, screen topology, visible states, alternate paths,
cancellation, failure, recovery, and terminal outcomes that matter.

Treat internal system work as a black box between an actor action and a visible
response. A flow may name `access denied`, `no results`, or another product
condition, but it must not show membership lookups, API or database calls,
query mechanics, cursor handling, retries, idempotency, or internal state that
has no visible effect.

Prefer labeled edges for navigation choices, permissions, availability,
validation, and other conditional paths. Use a diamond only when the interface
visibly asks a question and the answer is an observable user action. A user
action may label the outgoing edge. When several conditions route to different
surfaces, use one compact rectangular condition node. Keep runtime selection
logic in a rule, decision table, or sequence.

Keep one actor goal or closely related outcome in one flow. Use a short overview
and linked subflows when branches and crossing lines obscure the actor path.
Keep screen topology in the user-flow view; do not create a separate screen map.
For a headless or operator product, show actor actions and observable responses
without inventing screens.

Make each consequential user-visible surface explicit with a labeled visual
boundary such as `SURFACE · Match Feed` or, when referenced across files,
`SCREEN-001 · Match Feed`. Put the actions and visible states owned by that
surface inside its boundary, and label transitions between surfaces. This
surface-and-state inventory tells designers which pages, views, modals, panels,
or messages need mockups. Do not treat every flow node as a mockup: create a
mockup only when a surface or materially different state needs visual design.
The grouping communicates scope; it is not a wireframe. A project may use a
small, consistent vocabulary such as `VIEW`, `COMPONENT`, `DIALOG`, and
`EXTERNAL` to distinguish surface types, but these labels are not a required
taxonomy.

When a design file or system owns layout, styling, components, responsive
behavior, or interaction detail, put the exact mockup reference next to the
affected surface. Include the frame or node, version or branch when available,
and intent status. An authority-confirmed, in-scope mockup must be implemented,
not merely attached as a visual. Preserve its surface and component inventory,
content hierarchy, visible states, and interactions. Do not add, remove, merge,
split, or materially change them without accountable product or design approval.

When companion example, component, or export code exists, link it and prefer
reuse or adaptation when it is compatible with the repository. Generated or
exported code is implementation reference material, not design authority or
automatically production-ready code. Adapt it for repository conventions,
accessibility, security, and confirmed behavior without changing the approved
visible or interaction target. Raise a conflict instead of silently redesigning
the product. Flow surface groups still identify what needs design or a mockup;
Mermaid styling does not define or approve the product interface.

## Sequences

A sequence owns the detailed runtime coordination for one consequential
process. Include its actor action or system trigger, physical `ARCH-*`
participants, ordered sync or async messages, authority and data boundaries,
point of durable change, and material timeout, retry, fallback, duplication,
partial-failure, compensation, or human recovery behavior. This is the view
that explains how a process succeeds, degrades, retries, or recovers.

For every sequence that describes an implementable process, normally show a
compact DCL summary immediately below the `SEQ-*` introduction and above the
Mermaid fence:

```text
**DCL:** Target 3 (`confirmed`) · PIP current 5 (`inferred`) · Implementation current 4 (`inferred`, `git:0123456789abcdef0123456789abcdef01234567`)
**DCL gap:** PIP appears overbuilt; manual recovery is permitted by the confirmed target, while integrity protections remain required.
```

Show `not assessed` or `not implemented` when a current value is unavailable;
do not invent one or silently imply alignment. When an existing YAML record
owns the sequence, its optional `dcl` mapping is the structured owner and this
summary is the readable representation. When the Markdown sequence is the only
owner, the summary is sufficient; do not add a sidecar YAML file or registry
solely for DCL.

One DCL scope has one owner. Related capabilities, rules, data records, quality
constraints, user flows, and state machines link to that owner rather than
copying its levels or basis.

DCL describes the process's required engineering and operational
sophistication, not diagram length, documentation detail, code volume, or
completeness. A detailed sequence may describe a DCL 2 process and a short
sequence may describe a DCL 7 boundary. If a parent sequence coordinates
independently operated subprocesses with materially different DCLs, do not
average them or assign the highest child level to the parent. Give each child
its own focused sequence and level; assign the parent a level only when its
coordination is itself a coherent responsibility. Do not copy sequence DCL into
the linked state machine or user flow.

For an existing codebase, inspect the implementation before writing the
sequence. Keep physical systems as lifelines; use a message or adjacent note to
name the verified path and function, handler, job, or module that owns each
material step. Label the selected anchor `reuse unchanged` or `modify existing`.
Call for `new` code only after confirming that no suitable owner exists or that
an approved technical constraint requires separation. Do not map incidental
helpers or create a complete call graph. A note such as `modify existing:
path/to/file::function_name` is enough.

The existence of a path or symbol is an `observed` implementation fact. A
requirement to `reuse unchanged`, `modify existing`, or add a separate owner is
a target constraint and must remain `proposed` unless confirmed by accountable
technical authority or explicit project guidance.

For each consequential input, state its origin in the message or a short note:
user input and surface, parameter or return from a named function, persisted
field, external response or event, or named constant, configuration, or setting.
Include values that affect a branch, durable change, visible outcome, or
acceptance. Labels such as `store_id <- user selection`, `limit <- MATCH_LIMIT
setting`, or `rows <- load_rows() return` are sufficient. Do not list every
local variable or reproduce complete signatures.

When terms such as `eligible`, `safe`, `valid`, or `shared` affect a branch or
population, name the exact domain and processing stage. Distinguish, for
example, matching eligibility, model compatibility, actor authorization, and
public presentability; distinguish shared data or configuration from a shared
algorithm, population, lifecycle, or output. A rule at projection or
publication does not change retrieval or ranking membership unless confirmed
target intent explicitly says so.

Use the physical client as a participant. A `SCREEN-*` identifies the starting
or resulting surface; it is not a runtime lifeline. Return relevant facts once
and link to the rule or decision table that selects among visible outcomes
instead of repeating the same messages in many UI branches.

Split sequences only when message order, ownership, or recovery materially
differs. A sequence may name the durable state transition it causes, but it
must not restate the lifecycle model. Do not create one for a local interface
change or restate navigation or entity relationships inside it.

When a process proposes an explicit application-controlled database lock,
advisory lock, application-required isolation stronger than the project or
database default, singleton requirement, global queue constrained to one active
job or consumer, or another limit that serializes otherwise independent work,
treat that restriction as exceptional.
Show it in the owning sequence only when it materially affects correctness,
capacity, latency, recovery, or which processes can proceed. Name the minimum
needed to justify it:

- the invariant and concrete race or failure it prevents, linked to the owning
  rule or data constraint when one exists;
- the narrowest row, key, tenant, or other scope and the affected processes;
- why a uniqueness or exclusion constraint, atomic conditional statement,
  optimistic version check, idempotency, short transaction, or partitioned work
  does not protect the same invariant more simply.

Add acquisition and release, maximum hold or wait, timeout, recovery,
contention, and product or infrastructure cost only when they materially affect
the confirmed outcome or capacity bound.

Prefer the simplest correct mechanism that lets unrelated work proceed in
parallel. Do not make holding an explicit lock across external network or other
slow I/O a confirmed requirement without a specific invariant and explicit
latency and failure tradeoff. Do not serialize unrelated rows, tenants, jobs, or
processes to defend against a hypothetical race, and do not make larger database
infrastructure the default remedy for contention created by the design.
Ordinary short-lived locks that the database uses internally for atomic
statements and constraints are not an application-level restriction and do not
need PIP detail unless their contention becomes product-significant.

## State machines

A state machine owns stable lifecycle states, triggers, guards, permitted and
forbidden transitions, and material failure or recovery states. Do not model
every loading or display variant as durable state when it is derived from other
facts.

Use the state machine as the high-level map of how consequential processes move
an object through its lifecycle. Name the triggering action or process and,
when useful, link the transition to the `SEQ-*` that performs it. Show a failure
or recovery state only when it is durable or product-significant. Do not expand
a process's retries, fallback attempts, timeouts, ordered calls, or other
internal branches in the state machine; those belong in its sequence.

When a transition crosses physical services, name where it is initiated, where
it becomes valid or durable, and which system executes or observes it. Do not
put screen navigation, database fields, or ordered service messages in the
state diagram.

## Data models and ERDs

Use one data-model view for conceptual relationships and persisted entities.
Show identity, ownership, relationships, cardinality, and product-significant
constraints. Keep conceptual `DOM-*` and persisted `DATA-*` meanings distinct
when both are needed, even if one diagram shows their mapping.

Do not use the ERD to describe navigation, message order, transition validity,
or a full database definition. Add schema detail only when fields, constraints,
retention, migration, or compatibility are product-significant.

Before showing a persisted product classification as confirmed, ensure the
owning target fact defines its meaning, affected population, owner and update
lifecycle, and consumers. An observed field may be shown as implementation
evidence, but its presence in the schema does not make its semantics product
doctrine.

### Product-significant index notation

When an index is product-significant, use one combined convention: mark its
columns in the standard entity attribute table and define it in an `INDEXES`
compartment directly below that entity. The badges and compartment are a pair;
do not use a detached index list that leaves affected columns implicit.

On each participating attribute row:

- show `[I1·1]`, `[I1·2]`, and similar badges for an ordinary performance index;
- use `U` for a unique index or constraint and `P` for a partial, expression,
  or otherwise specialized index;
- use the number after `·` for the column's order in the index;
- mark a predicate-only column with `·where`, an included column with `·inc`,
  and a source column used only by an index expression with `·expr`;
- show every badge when a column participates in more than one index; and
- use the same color for a badge on the attribute and in the compartment, while
  preserving the textual identifier so the diagram never relies on color alone.

In the corresponding compartment, repeat the badge and show only known details
that matter: observed, proposed, confirmed, or stale status; physical index name
when known; uniqueness and method; ordered keys and direction; predicate or
expression; included columns; verified owning query or process when relevant;
and the product purpose through a direct `SEQ-*`, `RULE-*`, `QC-*`, or other
useful link. State a read/write, cost, or capacity tradeoff only when it
materially constrains the decision. A proposed record may state access and index
intent without inventing a physical definition. Use an outlined badge labeled
`PROPOSED` for an unconfirmed candidate and visibly mute a stale index. Include
a small legend once per diagram or board. Treat `P` as a visual category, not a
claim that the index cannot also be unique; the compartment owns the full
physical definition when it has been decided.

An index supports an owning product rule; it cannot establish the rule. A
partial-index or constraint predicate that changes admission, eligibility, or
population membership requires an independently confirmed target fact. Do not
use an agent-authored index proposal, migration, ticket, or test as authority
for the product classification encoded by its predicate.

For example:

```text
ATTRIBUTE               TYPE   KEY / CONSTRAINT   INDEX BADGE
match_id                 UUID   FK                 [P1·1]
publication_request_id   TEXT   UK                 [U2·1]
token                    TEXT   UK                 [U1·1]
disabled_at              TIME                      [P1·where]

INDEXES
[U1] CONFIRMED  pitch_card_token_key
     UNIQUE BTREE (token ASC)
     Supports SEQ-008: stable public-token lookup

[U2] CONFIRMED  pitch_card_publication_request_key
     UNIQUE BTREE (publication_request_id ASC)
     Supports SEQ-002: replay-safe publication

[P1] CONFIRMED  pitch_card_one_active_per_pitch_idx
     UNIQUE BTREE (match_id ASC) WHERE disabled_at IS NULL
     Supports SEQ-001: at most one active page per Match
```

Inspect the current schema, migrations, and owning queries before showing a
physical index. Do not invent a scale target or turn a candidate into confirmed
intent. Omit indexes that are routine implementation details, including an
ordinary primary-key backing index already communicated by `PK`, unless its
physical behavior is independently product-significant. If the authoring tool
cannot color individual cells, keep the textual badges. If it cannot create an
entity compartment, put the matching Markdown `INDEXES` table immediately below
the diagram in the same `.md` file. Do not change diagram type or add an artifact
solely to add color. Badge IDs are local visual labels unless another artifact
genuinely needs to reference them. A `PK`, `FK`, or `UK` label states schema
meaning and does not by itself prove that a separate physical index exists on
that column.

## Stack context and deployment

Stack context is the sole system-context diagram. Show actors, the product
boundary, external systems, physical clients, deployed services, workers,
managed platforms, stores, queues, and their labeled connections. State each
node's responsibility and owned state. Name a provider or runtime only when it
is confirmed.

When database connection use is product-significant, show or note which
deployed services, workers, and jobs connect and consider aggregate fan-out from
each bounded pool across replicas, autoscaled instances, and overlapping work,
plus dedicated or long-lived sessions. Before confirming multiple database
clients or pools inside one process, check whether they can reuse one bounded
process-level pool or consolidate without serializing useful work, causing
head-of-line blocking, or breaking session semantics. Preserve separate bounded
connections or pools when concurrent transactions, listeners or subscriptions,
long queries or streams, or workload isolation require them. Keep ordinary pool
checkout mechanics out of sequences unless exhaustion, waiting, or a dedicated
session changes process behavior or recovery. Record only confirmed provider
limits or material bounds; otherwise state bounded-reuse intent without
inventing pool sizes or requiring load-test ceremony.

Place security and operational controls on the node, connection, or trust zone
where they apply. Do not draw logical APIs, events, data records, policies, or
capabilities as peer services. Show ordinary deployment placement in this view.
If a separate deployment view is necessary, reuse the same `ARCH-*` IDs and
show only the added topology without repeating responsibilities.

## Decision tables

Use one decision table when several facts select an outcome. Let it own
condition precedence and resulting `SCREEN-*`, `SM-*`, action, or refusal.
Flows show the actor-visible result, sequences return the required facts, and
acceptance scenarios test representative combinations. Do not duplicate the
condition matrix in those artifacts.

## Optional journey maps

Create a product journey only when time, phases, recurrence, role changes, or
handoffs add meaning beyond a focused user flow. Keep actor actions and product
responses at lifecycle granularity and link detailed flows rather than copying
them.

For a research-based current-state journey, follow exactly these safeguards:

1. Create it only when placing evidence across time or touchpoints reveals
   context, transitions, or handoff problems a focused flow cannot show.
2. Mark it `observed` or `inferred` and identify it as an as-observed view; do
   not present it as intended behavior.
3. Include thoughts, emotions, friction, and workarounds only when evidence
   supports them; link the source and distinguish direct evidence from
   researcher inference.
4. Keep findings and opportunities separate from candidate product responses
   and current product decisions.

Store a journey as editable Markdown containing a lifecycle table, a fenced
Mermaid diagram, or both. Add stable IDs only for journey parts referenced by
another file.

## Design-board guidance

A design board supports review; it does not replace canonical PIP records.
Organize it so a reviewer can move through: target and legend, actors and
outcomes, journeys when used, flows, screens and states, shared patterns,
decisions and open questions, then archived material.

Show the stable ID, intent status, and canonical link on any board item that is
referenced elsewhere. During reconstruction, visibly separate as-observed,
intended-current, and target-next views. Keep blocked questions next to the
affected outcome. Never leave a build-affecting rule or decision only on the
board.

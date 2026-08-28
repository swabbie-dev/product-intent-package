# Development Complexity

## Purpose

Development Complexity Level (DCL) is an optional shorthand for comparing:

- the lowest engineering sophistication justified by confirmed product needs;
- the sophistication currently demanded by the PIP; and
- the sophistication embodied by an assessed implementation.

DCL helps expose under-specification, incomplete implementation, and
overbuilding. It is not a product score, company-maturity score, readiness
gate, acceptance criterion, or substitute for explicit requirements.

## Scope before level

Assign DCL to the smallest coherent responsibility whose behavior and
operation can be assessed together, such as one user-facing path, background
process, integration, service responsibility, data-serving boundary, or
sequence. Do not assign a blanket level to the product or inherit a level from
a connected process. Give each scope one owning YAML record or one owning
Markdown sequence summary; related artifacts link to it rather than copying the
values.

Before selecting a level, establish:

- the target release, actors, and actual user interactions;
- whether a user waits for or immediately depends on the work;
- acceptable delay, interruption, degradation, and downtime;
- failure consequence, reversibility, and blast radius;
- whether manual operation, retry, or recovery is acceptable;
- current and credible near-term volume, growth, and concurrency;
- data sensitivity, authorization, security, privacy, and compliance needs;
- required isolation, compatibility, and external commitments; and
- justified operating cost and maintenance burden.

These are evidence questions, not numeric dimensions to average. Choose the
lowest level that safely satisfies the confirmed needs. Reassess when those
needs or interactions materially change.

## Ordinal scale

Use whole levels from 1 through 10. The names are memory aids, not business
stages or feature checklists.

| Level | Illustrative operating posture |
| --- | --- |
| 1 | Idea test or manual experiment; disposable and directly supervised |
| 2 | Prototype proving a narrow interaction or technical path |
| 3 | Controlled pilot; limited users, acceptable interruption, and manual recovery |
| 4 | Minimal production product; core-path reliability and common-failure recovery |
| 5 | Repeatable early operation; routine work is supportable without constant intervention |
| 6 | Scaling operation; demonstrated load, bounded automation, and stronger operational recovery |
| 7 | Growth platform; several teams or workloads require stable ownership and compatibility |
| 8 | Midsize multi-region or similarly demanding platform operation |
| 9 | Global enterprise operation with stringent continuity, governance, or integration needs |
| 10 | Hyperscale or exceptional criticality requiring substantial custom infrastructure |

Do not add queues, caches, orchestration, regions, formal SLO machinery, or any
other feature merely because an illustrative level mentions a similar posture.
Name the exact behavior or quality requirement that justifies each material
mechanism. A demanding security or integrity requirement applies wherever its
risk exists; it does not raise unrelated processes or disappear at a low DCL.

## Mixed-scope example

One early product may reasonably use all of these levels at the same time:

| Responsibility | Product context | Illustrative target |
| --- | --- | --- |
| Offline preparation | No user waits; work may stop; operators can retry manually | 3 |
| Publication boundary | Changes durable public state and must prevent duplicate or corrupt publication | 4 |
| User-facing corpus retrieval | Interactive reads over a large, rapidly growing corpus must remain bounded | 6 |

The scalable retrieval need does not require generalized orchestration in
offline preparation. Acceptable manual recovery upstream does not weaken
publication integrity or unsafe-input protections. Assess and confirm each
scope independently; do not average these values or report their maximum as the
product's DCL.

## Optional record

Use the optional `dcl` mapping defined in the
[Package Standard](product-intent-package-standard.md#optional-scoped-development-complexity)
on the one YAML record that owns the scope. Only `target` is doctrine.
`pip_current`, `implementation_current`, and `gap_note` are inferred analysis.
A confirmed target is covered by the reviewed package confirmation or a more
specific linked `DEC-*`; do not create a decision merely to repeat package
confirmation.

Keep the local `basis` short and specific. Cite the assessed implementation
snapshot in `implementation_current.source_ref`. Omit an unassessed value
instead of inventing it, and say `not implemented` or `not assessed` in a
human-facing summary so absence is not mistaken for alignment. Update
`pip_current` when its owning PIP logic changes and update
`implementation_current` only after reviewing the cited implementation.

When known values differ, `gap_note` states whether the comparison suggests an
intentional stage-appropriate omission, a PIP deficiency, incomplete
implementation, possible overbuilding, or unresolved context. It does not
authorize a change. Route a material target choice through normal `OPEN-*` and
`DEC-*` records and implementation work through the task system.

## Sequence convention

Recommend DCL for every sequence that describes an implementable process. In a
Markdown sequence file, place a compact summary immediately below the `SEQ-*`
heading and introductory sentence and immediately above its Mermaid diagram:

> **DCL:** Target 3 (`confirmed`, `DEC-012`) · PIP current 5 (`inferred`) ·
> Implementation current 4 (`inferred`,
> `git:0123456789abcdef0123456789abcdef01234567`)
>
> **DCL gap:** PIP appears overbuilt; manual recovery is permitted by the confirmed
> target, while integrity protections remain required.

When an existing YAML record owns that sequence, keep the structured `dcl`
mapping there and treat the Markdown summary as its readable representation,
not a second authority source. When the Markdown sequence is the only owning
record, its summary is sufficient; do not add a sidecar YAML file or registry
merely to store DCL. Keep the values together when either representation
changes. When a current value is unavailable, show `not assessed` rather than
omitting the category from the summary.

One sequence should normally describe one coherent process with one DCL mapping
or summary. When independently operated subprocesses require materially
different levels, give each detailed process its own linked sequence and let a
parent sequence show their high-level interaction. Do not copy a sequence's DCL
onto a user flow or state machine merely because they link to it.

## Interpret differences

| Comparison | Review signal |
| --- | --- |
| Target = PIP = implementation | Rough complexity alignment; explicit requirements still decide correctness |
| Target > PIP | The PIP may not yet express the required development stage |
| PIP > target | The PIP may demand unnecessary complexity |
| PIP > implementation | Implementation may be incomplete or intentionally simpler |
| Implementation > PIP or target | The implementation may contain unsupported complexity or a legitimate unrecorded constraint |

A numeric difference never proves the diagnosis. Inspect the named basis and
exact requirements. Do not lower a target to make an existing design appear
appropriate, and do not delete harmless existing machinery solely to reduce a
number when removal would create more cost or risk than retaining it.

DCL does not replace acceptance, quality constraints, sequence logic, data
rules, or product authority. It explains the rough sophistication expected for
one scope so readers can distinguish deliberate stage-appropriate omissions
from likely accidents.

# Development Complexity

## Purpose

Development Complexity Level (DCL) is optional shorthand for the general
engineering and operational sophistication the current product intent requires.
It helps developers and architects understand the product's stage and whether a
simple design is deliberate. It is not a product score, company-maturity score,
readiness gate, acceptance criterion, or feature checklist.

## Product default, narrow override

When DCL is useful, put one default in `product.yaml`:

```yaml
dcl:
  level: 4
  basis: >-
    Users rely on the core path in production, common failures need automatic
    recovery, and current load does not justify generalized scale machinery.
```

The default applies to the whole product unless a narrowly defined area has
materially different needs. Different parts may require different levels, but
do not assign a level to every record. Add a local override only where user
interaction, failure consequences, recovery, real load, data sensitivity,
security, compliance, or operational demands justify it:

```yaml
dcl_override:
  level: 6
  basis: >-
    Interactive retrieval serves a rapidly growing corpus and must remain
    bounded while users wait.
```

The narrow owner may be a capability, rule, data boundary, quality constraint,
or process. Related artifacts link to that owner rather than copying its level.
Do not average overrides, raise the product default to the highest exception, or
inherit one process's exception across connected areas.

## Choose the level from the product

Before selecting a level, establish:

- the release, actors, and actual user interactions;
- whether a user waits for or immediately depends on the work;
- acceptable delay, interruption, degradation, and downtime;
- failure consequence, reversibility, and blast radius;
- whether manual operation, retry, or recovery is acceptable;
- current and credible near-term volume, growth, and concurrency;
- data sensitivity, authorization, security, privacy, and compliance needs;
- required isolation, compatibility, and external commitments; and
- justified operating cost and maintenance burden.

These are judgment inputs, not numeric dimensions to average. Choose the lowest
level that safely satisfies the current intent. Reassess when users,
interactions, risks, or credible load materially change.

## Decide edge-case handling separately

DCL does not determine whether a rare or complex edge case deserves automatic
handling. When the PIP does not already resolve the case, ask the product
manager, originator, or other human product authority before designing,
implementing, or extensively testing it. Clarify which current behavior is
intended:

- handle it automatically;
- contain it and route it to manual review, intervention, or recovery;
- fail or defer visibly with a defined next action; or
- exclude the case from the current release.

Apply this question at every DCL. Low DCL does not automatically justify manual
handling, and high DCL does not automatically justify elaborate automation for
a rare case. Consider frequency, user impact, time sensitivity, detectability,
reversibility, operating burden, and the cost and complexity of reliable
automation. Record the chosen behavior in the PIP artifact that owns the
affected flow, acceptance, process, state, or quality constraint before chasing
implementation detail.

Manual review is valid when it is an intentional product or operating path and
the system can safely contain the case until a human acts. It is not a reason to
allow an authorization, security, privacy, money, data-integrity, or destructive
effect to occur before review. Preserve the smallest automatic protection
needed to prevent that harm, even when final resolution is manual.

For a manual fallback, the default product requirement is visibility: make the
responsible admin or operator aware that the incident occurred and provide
enough context to identify it, understand the safe current state, and locate the
existing investigation or recovery procedure. Prefer the smallest reliable,
monitored notification path already available. A log entry by itself is not
sufficient when no person or alerting process is expected to notice it.

Do not infer that manual handling requires a dedicated admin dashboard, inbox,
queue, detail page, retry button, editor, override, or control for every case.
Add product-specific controls only when the approved manual procedure requires
an action that existing operational tools cannot safely perform, or when the
case's frequency, urgency, or volume makes the control worthwhile. The PIP owns
the visibility and product outcome; a runbook or implementation note may own
the incidental operating steps.

## Ordinal scale

Use whole levels from 1 through 10. The names are memory aids, not business
stages or feature requirements.

| Level | Illustrative operating posture |
| --- | --- |
| 1 | Idea test or manual experiment; disposable and directly supervised |
| 2 | Prototype proving a narrow interaction or technical path |
| 3 | Controlled pilot; limited users, acceptable interruption, manual recovery |
| 4 | Minimal production product; core-path reliability and common-failure recovery |
| 5 | Repeatable early operation; routine work is supportable without constant intervention |
| 6 | Scaling operation; demonstrated load, bounded automation, stronger operational recovery |
| 7 | Growth platform; several teams or workloads require stable ownership and compatibility |
| 8 | Midsize multi-region or similarly demanding platform operation |
| 9 | Global enterprise operation with stringent continuity, governance, or integration needs |
| 10 | Hyperscale or exceptional criticality requiring substantial custom infrastructure |

Do not add queues, caches, orchestration, regions, SLO machinery, or another
mechanism merely because a level mentions a similar posture. Name the exact
product or quality requirement that justifies material machinery. A demanding
security or integrity requirement applies wherever the risk exists; it neither
raises unrelated work nor disappears at a low DCL.

## Mixed product example

An early product might use default DCL 4 while narrow areas differ:

| Scope | Product context | DCL |
| --- | --- | --- |
| Product default | Small production product; common failure recovery; modest current load | 4 |
| Offline preparation override | No user waits; work may stop; operators can retry manually | 3 |
| Retrieval override | Interactive reads over a large, rapidly growing corpus must remain bounded | 6 |

The retrieval exception does not justify generalized orchestration in offline
preparation. Manual upstream recovery does not weaken publication integrity or
unsafe-input protections. Keep each override narrow and explain its current
reason.

## Sequence convention

Recommend a visible DCL line for every implementable sequence, immediately
above its Mermaid diagram:

> **DCL:** 4 (product default)

or:

> **DCL override:** 6 — Interactive retrieval must remain bounded while users wait.

The first line points to `product.yaml.dcl`. The second is owned by that
sequence. Do not repeat the sequence's override on its linked user flow or state
machine. Diagram length, code volume, and documentation detail do not determine
DCL.

## Implementation comparison stays outside the PIP

An audit or task note may compare target and observed implementation levels:

```text
PIP target DCL: 4 (product default)
Observed implementation DCL: 6 at git:<revision>
Finding: the implementation includes generalized orchestration not required by
the current product; preserve named integrity protections while reviewing the
extra machinery.
```

This comparison is implementation analysis, not product intent. Do not put the
observed level, gap, source revision, or alignment status in the PIP. A numeric
difference is only a review signal; inspect exact requirements before changing
anything. Do not lower the target to make existing code appear appropriate, add
machinery to match a number, or remove harmless machinery when removal costs
more than retention.

DCL never replaces acceptance, quality constraints, sequence logic, data rules,
or product authority. Exact current requirements always decide correctness.

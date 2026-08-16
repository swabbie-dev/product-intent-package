# Authority Questioning Protocol

## Objective

Convert missing or ambiguous product intent into small, authoritative, testable decisions without interrogating stakeholders about facts already present in evidence.

## Question unit

Each question should contain only the information needed to decide:

```text
Decision needed: <one build-affecting choice>
Why it matters: <affected behavior or handoff risk>
Evidence: <relevant source IDs and conflict, if any>
Authority: <named accountable person/role>
Options: <only when useful; include consequences>
Question: <direct request for a decision>
```

Do not bury multiple independent decisions in one question.

## Batching

Batch related questions when the answers do not depend on one another. Ask sequentially when an answer changes the next branch.

Good batches:

- release scope and excluded capabilities;
- all states and transitions for one domain object;
- all screen states for one flow;
- all measurable quality targets for one critical operation.

Bad batches:

- dozens of unrelated questions;
- product, visual, and infrastructure decisions addressed to one person without confirming authority;
- questions whose answers already exist in a confirmed decision.

## Confirmation loop

1. Receive the answer.
2. Translate it into a diagram/table/schema/rule.
3. Restate only the normalized decision and observable consequences.
4. Ask for confirmation when normalization introduced interpretation.
5. Record the decision and update dependent artifacts.

A direct, unambiguous answer from the accountable authority may be recorded without a redundant confirmation round. Ambiguous answers may not.

## Proposal discipline

The agent may propose:

- a likely interpretation;
- a clean default;
- options with tradeoffs;
- a design or technical recommendation.

Label every proposal. Do not write it into active canonical intent until confirmed or covered by delegation.

## Exhaustion techniques

Use these techniques to expose unstated assumptions:

| Technique | Question pattern |
|---|---|
| actor walk-through | “Starting from no session/data, how does `ACTOR-*` complete `CAP-*`?” |
| state exhaustion | “What states can this object occupy, and what triggers every transition?” |
| branch inversion | “What happens when each precondition is false?” |
| failure drill | “What happens before, during, and after timeout, partial failure, retry, and cancellation?” |
| authority boundary | “Is this product behavior, design choice, technical choice, or delegated discretion?” |
| data lifecycle | “When is this created, changed, retained, exported, archived, restored, and deleted?” |
| concurrency drill | “What happens if this is repeated, duplicated, reordered, or performed simultaneously?” |
| permissions matrix | “Who can see, create, modify, approve, revoke, and audit this in every account state?” |
| temporal drill | “Which clock/time zone governs it? What occurs at boundaries, expiration, pause, and resume?” |
| counterexample | “Give one valid and one invalid example near the boundary.” |
| acceptance inversion | “What observable result would prove this implementation wrong?” |

## Question-complete criterion

A topic is not complete merely because no stakeholder volunteered more detail. It is complete when:

- all applicable coverage lenses have an explicit representation or confirmed exclusion;
- all related artifacts are confirmed and internally consistent;
- every behavior can be expressed as an acceptance result;
- the coding orchestrator has no unbounded choice that could change externally observable behavior.

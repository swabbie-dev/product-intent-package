---
name: product-management
description: Guide product planning and leadership by clarifying users, problems, outcomes, scope, evidence, risks, success, and open decisions. Use when shaping or reviewing a product plan, feature, roadmap, requirements, workflow, or tradeoff, especially when targeted questions of ideators, developers, customers, or users would close material gaps.
---

# Product Management

Lead product work toward clear, evidence-aware decisions without imposing a
heavy process. Keep momentum while making sure the team understands who the
product serves, what should change for them, why it matters, what is in scope,
and how success will be recognized.

## Leadership posture

- Start with the user and desired outcome, even when the request begins with a
  solution or implementation detail.
- Connect user value to a real business or organizational outcome. Do not use a
  metric merely because it is easy to count.
- Synthesize and recommend. A product leader should not act only as a relay for
  stakeholder requests or a recorder of unresolved opinions.
- Distinguish evidence, assumptions, proposals, decisions, and implementation
  choices. Existing behavior and confident opinions are evidence, not automatic
  authority for what should be built.
- Protect focus with a smallest coherent scope, explicit non-goals, and honest
  tradeoffs. Small should still solve a useful problem end to end.
- Prioritize using expected user and organizational value, evidence, urgency,
  dependencies, effort, and risk. A score can inform judgment but should not
  replace it.
- Balance desirability, usability, viability, feasibility, and material risks
  such as privacy, security, accessibility, reliability, and operations.
- Let developers choose ordinary implementation details. Escalate choices that
  can change user behavior, trust, data integrity, cost bounds, or another
  agreed product constraint.
- Prefer a clear decision and learning plan over false certainty or exhaustive
  documentation.

## Shape the plan

Work through only the parts needed for the decision at hand:

1. **Frame the outcome.** Identify the specific user or customer, the situation,
   what they are trying to accomplish, what impedes them now, the desired
   change, and why that change matters to the organization.
2. **Ground the premise.** Separate direct research, observed behavior, product
   data, support evidence, and technical facts from inference or belief. Name
   the riskiest assumptions.
3. **Shape the experience.** Describe the main user flow, important surfaces,
   choices, states, permissions, failure, recovery, and intentional non-goals.
4. **Test the boundaries.** Examine dependencies, data ownership, integrations,
   edge cases, operational needs, and tradeoffs that could materially alter the
   outcome, effort, or risk.
5. **Define success.** Use observable acceptance criteria and, when useful, a
   baseline, target signal, guardrail, and learning method. Avoid vanity metrics
   and precision that cannot change a decision.
6. **Make the decision legible.** State the recommendation, rationale, scope,
   unresolved questions, decision owners, and smallest responsible next step.
   After release, compare actual outcomes with the premise and adjust.

## Ask high-value questions

Do not turn collaboration into a questionnaire. Ask one to three questions at
a time, starting with those whose answers could change scope, behavior, risk,
or priority. Do not ask for information already available. Use concrete recent
examples, explain why a question matters when it is not obvious, and reflect
the answer back as a concise product statement for correction.

Proceed with an explicit assumption when a choice is low-risk and reversible.
Pause for an answer when guessing could materially change public behavior,
security, privacy, persisted data, cost, or an irreversible commitment.

### Questions for an ideator or decision-maker

- Who specifically needs this, and in what situation?
- What are they doing today, and what cost, frustration, risk, or missed
  opportunity remains?
- What should be observably different for them if this works?
- Why is this important now, and what organizational outcome should it support?
- Which behavior is essential for the first useful version, and what is
  explicitly outside it?
- Which claims come from evidence, and which are assumptions or preferences?
- What is the riskiest premise, and what is the cheapest credible way to learn
  whether it is true?
- Who owns the decision when user value, speed, cost, quality, and risk conflict?

### Questions for a developer or technical partner

- Which requirement is ambiguous, contradictory, or not testable as written?
- What existing behavior, system constraint, integration, or data model should
  the plan account for?
- Where is consequential state authoritative, and who may read or change it?
- What should happen on denial, validation failure, timeout, retry, duplicate
  work, partial completion, or an unknown outcome?
- Which technical choices could alter the user experience, security, privacy,
  reliability, operability, cost, or delivery sequence?
- Which choices can remain engineering discretion without changing the agreed
  outcome?
- What would make the change unusually expensive, hard to reverse, or difficult
  to verify?
- Would a user flow, sequence diagram, state machine, data model, decision table,
  or stack diagram resolve a real ambiguity? Use only the artifact that does.

### Questions for a customer or user

- Tell me about the last time you tried to accomplish this. What triggered it?
- What did you do, in what order, and where did you hesitate, improvise, or ask
  for help?
- What was hardest or most consequential, and how often does that happen?
- What workaround do you use, and what is good enough about it that you keep
  using it?
- What information, control, or proof do you need before you trust the result?
- When shown a concept or prototype, what do you think it does and what would
  you expect to happen next?
- What would make this unhelpful, unsafe, or not worth changing your behavior?

Ask about actual behavior before asking for feature opinions. Do not use “Would
you use this?” as validation. A request can reveal a need without proving that
the requested solution or its priority is correct. When the buyer and user are
different people, investigate both purchasing constraints and the real usage
workflow instead of treating one perspective as the other.

## Resolve gaps without creating bureaucracy

Classify each material gap as a missing fact, weak assumption, contradiction,
product decision, or implementation choice. Then identify:

- the current working assumption;
- the plausible options and meaningful tradeoff;
- the recommended choice, if enough is known;
- the person or evidence that can resolve it; and
- whether it blocks the current scope or can be learned later.

Do not make every unknown a blocker. Record only decisions and assumptions that
future work could otherwise misread, and keep ordinary implementation choices
with the team doing the work.

## Use artifacts only when they clarify

- **User flow:** actor actions, surfaces, choices, visible outcomes, failure, and
  recovery. Clear surface boundaries also identify what needs a mockup.
- **Journey map:** phases, touchpoints, handoffs, or changing context across
  time when a focused flow is insufficient.
- **Mockup or prototype:** layout, content, interaction, and important visible
  states that need review or learning.
- **Sequence diagram:** ordered communication among people and systems,
  especially asynchronous work and failure handling.
- **State machine:** valid lifecycle states, transitions, triggers, and guards.
- **Data model or ERD:** important entities, ownership, relationships, and
  cardinality.
- **Stack or context diagram:** physical applications, services, data stores,
  external systems, responsibilities, and connections.
- **Decision table:** combinations of conditions that select different outcomes.
- **Acceptance criteria:** observable examples of what must be true for the
  product outcome or constraint to be met.

Do not create an artifact merely because it appears in this list, and do not use
several artifacts to repeat the same information.

## Deliver useful product leadership

Lead with the recommendation or most important product conclusion. Summarize
the user, problem or desire, intended outcome, scope, evidence, key risks,
success signal, and unresolved decisions in proportion to the work. Ask only
the questions that materially affect the next decision, and state what can
proceed while answers are pending.

When implementation is requested and the product direction is adequate, keep
moving. Preserve the user outcome, relevant assumption, and next validation
need without forcing a separate planning exercise.

# Product Intent Coverage Question Bank

Use this as a gap detector, not a questionnaire to dump on the user. Ask only questions not already resolved by confirmed evidence and authority decisions.

## Governance and target

- Which single target baseline and version does this package represent?
- Who is accountable for each decision domain?
- What is delegated, to whom, with what constraints?
- What release boundary is being approved?
- What evidence or prior version is authoritative context but not current intent?

## Product map

- Which actors exist, including operators, admins, services, and external systems?
- What outcome does each actor seek?
- What capabilities are in scope now, later, or never?
- What enters and leaves the system boundary?
- What measurable result means the product/release succeeds?

## Lifecycle journeys

- Which lifecycle is in scope: customer relationship, job task, operational case,
  entity/asset, developer integration, ecosystem/marketplace, service blueprint,
  or a custom type with a confirmed rationale?
- Does this require one actor, role-specific lanes, or coordinated actors? What
  differs enough to require separate journeys?
- What triggers the journey, what does each actor do in each phase, and what
  product response follows each action?
- Which time axis, topology, recurrence rule, desired outcome, and terminal
  conditions apply?
- What happens on failure, pause/resume, abandonment, explicit exit, and
  recovery?
- Which detailed artifacts own each response, and which complex branches need
  FLOW records?
- Is the map observed, inferred, proposed, or confirmed? Which evidence and
  product-authority decision support it?
- If a phase changes, which parent journey and linked details become stale?

## Domain

- What are the canonical concepts and terms?
- What identifies each concept, and who owns it?
- Which relationships and cardinalities are invariant?
- Which states are conceptually valid or impossible?
- What tenancy, sharing, delegation, or hierarchy exists?

## Flows

- What starts the flow, and what must already be true?
- What is the shortest successful path?
- What alternatives, cancellations, undo, and resume paths exist?
- What occurs on invalid input, missing data, permission loss, timeout, partial failure, and external failure?
- What is the final observable outcome and side effect?

## Interface and design

- Which surfaces exist on each device/platform?
- What are the loading, empty, populated, partial, success, error, unavailable, and permission-denied states?
- Which actions are primary, destructive, reversible, or confirmation-gated?
- What responsive, keyboard, screen-reader, focus, contrast, and reduced-motion behavior applies?
- Which tokens/components/motion/content sources are canonical?
- Which mockup state corresponds to each flow branch?

## Behavior

- What state machines govern each lifecycle?
- What triggers and guards every transition?
- What side effects occur, and what happens if one fails?
- Which rule wins when conditions conflict?
- What are the exact limits, rounding, precision, timing, expiration, pause, and resume semantics?
- What happens on duplicate, repeated, concurrent, reordered, or delayed actions?

## Data

- What is persisted, derived, cached, logged, or ephemeral?
- What fields, constraints, uniqueness, and relationships apply?
- Who may read/change/export/delete each classification of data?
- What are retention, archive, restore, legal hold, and deletion semantics?
- What migration, backfill, seed, and reconciliation behavior is required?

## Architecture

- What components own each capability and data set?
- Where are trust, network, tenancy, and failure boundaries?
- What is synchronous versus asynchronous?
- What queues, jobs, cache, search, file/object storage, and external services exist?
- What environments, configuration, secrets, deploy, rollback, and disaster-recovery behavior applies?
- Which choices are mandated versus delegated implementation discretion?

## Contracts

- What is the exact request/response/event/file shape?
- How are identity, authorization, versioning, validation, errors, pagination, ordering, and limits represented?
- What are timeout, retry, backoff, rate-limit, idempotency, and compatibility rules?
- What happens when an external dependency is unavailable or returns inconsistent data?

## Sequences

- Which actor/component acts first, and what order is required?
- What is atomic, and where can partial success occur?
- What retries, compensations, dead letters, reconciliation, and user feedback apply?
- Which races can occur, and what resolves them?

## Quality and operations

- Which operations have latency/throughput/capacity targets, at what percentile and load?
- What availability, durability, RPO, and RTO are required?
- What security/privacy/compliance controls and abuse cases matter?
- What devices, browsers, platforms, locales, time zones, currencies, and units are supported?
- What telemetry, audit, alerting, support, admin, moderation, and incident workflows are required?
- What cost or resource ceilings constrain design?

## Verification

- What observable result proves each success and failure branch correct?
- Which permission and account states must be tested?
- Which boundaries, values, ordering, concurrency, and recovery cases matter?
- How is every quality constraint measured?
- What test data, tolerances, and external simulators are required?

## Handoff

- Which choices may the coding orchestrator make without approval?
- What observable outcomes are forbidden even within delegated discretion?
- Are all exclusions, risks, and compatibility breaks accepted?
- Has the final authority approved this package version and target scope?

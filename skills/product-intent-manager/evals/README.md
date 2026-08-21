# Skill Evaluation Cases

Use the cases in `cases.yaml` to test both activation and behavior.

Minimum must-pass rubric:

- invokes for the intended workflow and not for ordinary code documentation/implementation;
- distinguishes evidence from confirmed intent;
- identifies and routes authority domains;
- refuses to silently infer behavior or resolve conflicts;
- produces all thirteen structures, including lifecycle journeys, and traceability;
- leaves unavailable decisions blocked rather than fabricating certainty;
- does not claim build-ready while review gates fail;
- records bounded implementation discretion rather than vague “best practices”;
- for iteration, marks dependent artifacts stale and updates acceptance and traceability;
- writes skill-authored structured records as `.yaml` and Mermaid diagrams as `.md` files with fenced `mermaid` blocks, including diagram-only files;
- keeps `.json` and `.mmd` only for copied source evidence or required external formats, not canonical package records.
- uses Product Intent Package format `5.0.0` for the consolidated diagram paths.
- keeps the five default diagram sources for stack context, user flows, state
  machines, data model/ERD, and sequences; populates each applicable diagram or
  records a confirmed not-applicable result; and adds deployment only when it
  needs a separate view;
- uses `architecture/stack-context.md` as the sole context diagram. It combines
  actors, the product boundary, external systems, physical services,
  responsibilities, owned state, labelled connections, and normally deployment
  placement;
- keeps product outcome, release boundary, exclusions, and measures in the
  scope and capability records rather than a second context diagram;
- merges screen topology and user flows in `experience/user-flows.md`, while
  retaining screen YAML and design-board records;
- merges conceptual domain relationships and the ERD in `data/data-model.md`,
  while keeping `DOM-*` and `DATA-*` IDs semantically distinct;
- uses `architecture/deployment.md` only when environment, region, network,
  failover, or rollout complexity makes stack context hard to understand. The
  separate view reuses stack-node IDs and shows affected connections or state
  without repeating responsibilities;
- keeps canonical state machines and allocates each cross-service transition to
  its initiator, durable authority, executor, observers, and recovery path;
- gives each allocated transition a stable local ID and uses transition-level
  traceability when needed;
- does not invent a provider or runtime, and preserves stable IDs while it
  updates moved paths and affected governance records;
- retires separate component, container, system-context, and screen-map
  diagrams after their unique content moves to the consolidated views;
- separates observable user experience, valid state, ordered runtime work, data
  structure, and physical topology; preserves context with shared IDs; and puts
  multi-condition outcome selection in one rule or decision table;

Additional journey rubric:

- distinguish a lifecycle journey from a marketing funnel;
- separate materially different actor variants;
- require an actor-action lane and a product-response lane for every action;
- cover failure, pause/resume, abandonment, exit, and recovery;
- keep observed, inferred, proposed, and confirmed journey intent separate;
- require qualified local links, detailed artifact links, and editable Markdown
  sources;
- mark the parent journey and linked dependents stale after phase changes;
- block build-ready and journey_closure for open journey questions, assumptions,
  contradictions, or unconfirmed intent.

These cases are prompts and review rubrics. No automated eval runner is
included.

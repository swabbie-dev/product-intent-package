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
- uses a physical runtime-stack map with named services, responsibilities,
  owned state, and labelled connections instead of a mixed logical component
  diagram;
- keeps system context limited to actors, the product boundary, and external
  systems;
- keeps canonical state machines and allocates each cross-service transition to
  its initiator, durable authority, executor, observers, and recovery path;
- gives each allocated transition a stable local ID and uses transition-level
  traceability when needed;
- does not invent a provider or runtime, and preserves stable IDs while it
  updates moved paths and affected governance records;
- retires canonical `architecture/components.md`, `architecture/containers.md`,
  and `architecture/deployment.md` after their unique content moves to
  `architecture/runtime-stack.md`;

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

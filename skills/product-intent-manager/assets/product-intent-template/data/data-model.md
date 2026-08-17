# Data model

Keep the conceptual domain model and physical data model in one file. A
conceptual `DOM-*` record may map to one or more physical `DATA-*` records.

## Conceptual domain model

```mermaid
classDiagram
  %% class DOM_001["DOM-001 Concept"] {
  %%   +field type
  %% }
  %% Use conceptual entities, relationships, ownership, and invariants.
```

## Physical ERD

```mermaid
erDiagram
  %% DATA_001 {
  %%   integer id PK
  %%   string value
  %% }
  %% Show physical entities, fields, keys, and relationships.
```

## Conceptual-to-physical mapping

| Domain concept | Physical record(s) | Mapping note |
| --- | --- | --- |
| `DOM-001` | `DATA-001` | Explain the mapping or record that it is unresolved. |

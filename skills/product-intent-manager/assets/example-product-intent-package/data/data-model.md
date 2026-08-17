# Data model

The conceptual counter maps to one physical singleton record.

## Conceptual domain model

```mermaid
classDiagram
  class DOM_001["DOM-001 Counter"] {
    +integer value
  }
  class DATA_001["DATA-001 CounterRecord"]
  DOM_001 --> DATA_001 : persists as
```

## Physical ERD

```mermaid
erDiagram
  DATA_001 {
    integer id PK
    integer value
    timestamp updated_at
  }
```

`DATA-001` is stored as `counter_record` in Supabase Postgres. The singleton
key and field constraints remain authoritative in `data/schema.yaml`.

| Domain concept | Physical record(s) | Mapping note |
| --- | --- | --- |
| `DOM-001 Counter` | `DATA-001 CounterRecord` | One conceptual counter maps to one singleton physical record. |

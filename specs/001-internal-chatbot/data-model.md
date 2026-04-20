# Data Model: Internal Support & Sales Chatbot

## Source Files (read-only at runtime)

### products.json

Array of product objects. Minimum expected fields:

| Field       | Type   | Notes                                    |
|-------------|--------|------------------------------------------|
| id          | string | Unique product identifier                |
| name        | string | Product display name                     |
| description | string | Full product description (embedded)      |
| category    | string | Product category (optional, for context) |

Additional fields may be present and will be passed to the LLM as-is.

### customers.json

Array of customer objects. Minimum expected fields:

| Field        | Type   | Sensitive | Notes                                         |
|--------------|--------|-----------|-----------------------------------------------|
| id           | string | No        | Unique customer identifier                    |
| first_name   | string | No        | Used for name-based lookup                    |
| last_name    | string | No        | Used for name-based lookup                    |
| email        | string | No        | Contact information                           |
| phone        | string | No        | Contact information                           |
| address      | string | Yes       | Physical address — LLM instructed to refuse   |
| password     | string | Yes       | Account credential — LLM instructed to refuse |
| bank_account | string | Yes       | Financial data — LLM instructed to refuse     |

Additional fields may be present. The LLM is instructed to refuse all sensitive fields regardless.

---

## Runtime Entities

### EmbeddingIndex (in-memory)

Holds pre-computed product embeddings loaded at application startup.

| Field      | Type          | Notes                                           |
|------------|---------------|-------------------------------------------------|
| embeddings | numpy ndarray | Shape (N, D) — one row per product              |
| products   | list[dict]    | Parallel list of raw product dicts              |

### ChatRequest

Input to the `/chat` endpoint.

| Field    | Type   | Validation         |
|----------|--------|--------------------|
| question | string | Required, non-empty |

### ChatResponse

Output of the `/chat` endpoint. Always returned, even on error.

| Field      | Type          | Notes                                    |
|------------|---------------|------------------------------------------|
| answer     | string or null | Null when no answer available            |
| confidence | float         | 0.0–1.0; model-assigned                 |
| error      | string or null | Null on success; describes failure cause |

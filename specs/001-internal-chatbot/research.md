# Research: Internal Support & Sales Chatbot

## Embedding-Based Product Search (RAG)

**Decision**: Use OpenAI `text-embedding-3-small` with cosine similarity via numpy.

**Rationale**: The product catalogue is small and static. Computing embeddings at startup and storing them
in a numpy array is the simplest possible RAG implementation — no vector database needed, no streaming,
no external indexing service.

**Alternatives considered**:
- FAISS: Overkill for a small static dataset; adds a C++ dependency.
- sentence-transformers (local): Adds a large model download; OpenAI API already in the stack.
- chromadb / pinecone: External service dependencies; violates Simplicity principle.

---

## Customer Name Lookup

**Decision**: Case-insensitive substring match on `first_name`, `last_name`, and concatenated full name
from customers.json. Loaded once at startup.

**Rationale**: The spec requires lookup by first name, last name, or full name. A simple string search
covers all three cases without additional dependencies.

**Alternatives considered**:
- Fuzzy matching (rapidfuzz): Adds complexity; not required by spec.
- Database full-text search: No database in this project.

---

## Language Model

**Decision**: `gpt-4o-mini` via the OpenAI Python SDK. Structured JSON output via `response_format={"type": "json_object"}`.

**Rationale**: Cost-effective for an internal tool. JSON mode guarantees the three-field response schema
(`answer`, `confidence`, `error`) without post-processing heuristics.

**Alternatives considered**:
- `gpt-4o`: More capable but unnecessary for this use case; higher cost.
- Local LLM (Ollama): Requires infrastructure; violates Simplicity principle.

---

## Sensitive Data Handling

**Decision**: Handled exclusively by the LLM via system prompt. No application-layer keyword filtering.

**Rationale**: The spec states "no other security is required". Delegating to the LLM is simpler and
avoids maintaining a keyword blocklist.

**Alternatives considered**:
- Regex/keyword blocklist: More maintenance burden; brittle; not requested by spec.

---

## Project Structure

**Decision**: Flat Python package at repository root. One module per responsibility.

**Rationale**: Small scope (one endpoint, two data sources, one LLM call). A deep `src/` hierarchy adds
navigation friction without benefit.

**Alternatives considered**:
- `src/` layout: Standard for larger projects; overkill here.
- Monorepo with separate packages: No second service exists; violates YAGNI.

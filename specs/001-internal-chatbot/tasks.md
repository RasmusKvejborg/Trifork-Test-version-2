---
description: "Task list for Internal Support & Sales Chatbot"
---

# Tasks: Internal Support & Sales Chatbot

**Input**: Design documents from `specs/001-internal-chatbot/`
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/api.md ✅

**Tests**: Automated tests are FORBIDDEN per the project constitution. Do not include any test tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1–US4)
- All paths are relative to the repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and static data files

- [x] T001 Create `requirements.txt` with pinned dependencies: fastapi, uvicorn[standard], openai, numpy, python-dotenv, pydantic
- [x] T002 [P] Create `.env.example` with placeholder `OPENAI_API_KEY=sk-...` (do not commit actual key)
- [x] T003 [P] Create `data/products.json` with at least 5 sample products (fields: id, name, description, category)
- [x] T004 [P] Create `data/customers.json` with at least 3 sample customers (fields: id, first_name, last_name, email, phone, address, password, bank_account)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and file loaders that ALL user story phases depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create `models.py` with Pydantic models: `ChatRequest` (field: question: str) and `ChatResponse` (fields: answer: str | None, confidence: float, error: str | None)
- [x] T006 Create `main.py` with FastAPI app, python-dotenv `.env` loading at startup, and `GET /health` endpoint returning `{"status": "ok"}`
- [x] T007 [P] Create `product_search.py` with `load_products(path: str) -> list[dict]` function that reads and returns `data/products.json`
- [x] T008 [P] Create `customer_lookup.py` with `load_customers(path: str) -> list[dict]` function that reads and returns `data/customers.json`

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 - Product Question (Priority: P1) 🎯 MVP

**Goal**: Employee asks a product question; system retrieves top-3 semantically relevant products and LLM answers based solely on that data.

**Independent Test**: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What does the volumizing mascara do?"}'` returns a non-null `answer` drawn from products.json, `confidence` > 0, `error` null.

### Implementation for User Story 1

- [x] T009 [P] [US1] Implement `embed_text(text: str, client: OpenAI) -> list[float]` in `product_search.py` — calls `text-embedding-3-small` and returns the embedding vector
- [x] T010 [P] [US1] Implement `build_index(products: list[dict], client: OpenAI) -> tuple[np.ndarray, list[dict]]` in `product_search.py` — embeds each product's `description` field, returns numpy array of shape (N, D) and parallel product list
- [x] T011 [US1] Implement `search_products(query: str, index: np.ndarray, products: list[dict], client: OpenAI, top_k: int = 3) -> list[dict]` in `product_search.py` — embeds query, computes cosine similarity against index, returns top-3 product dicts (depends on T009, T010)
- [x] T012 [US1] Create `chat_handler.py` with `build_prompt(question: str, products: list[dict], customers: list[dict]) -> list[dict]` — returns OpenAI messages list with system prompt and user message containing retrieved product and customer context (depends on T005)
- [x] T013 [US1] Implement `call_llm(question: str, products: list[dict], customers: list[dict], client: OpenAI) -> ChatResponse` in `chat_handler.py` — calls `gpt-4o-mini` with `response_format={"type": "json_object"}`, parses JSON into ChatResponse (depends on T012)
- [x] T014 [US1] Register FastAPI startup event in `main.py` — initialise OpenAI client, call `build_index()` to compute embedding index, call `load_customers()`, store all three on `app.state` (depends on T007, T008, T010)
- [x] T015 [US1] Implement `POST /chat` endpoint in `main.py` — calls `search_products()`, `lookup_customers()`, `call_llm()`, returns `ChatResponse`; reads client and index from `app.state` (depends on T011, T013, T014, T016)

**Checkpoint**: User Story 1 fully functional — product questions return accurate JSON answers

---

## Phase 4: User Story 2 - Customer Lookup (Priority: P2)

**Goal**: Employee asks about a customer by name; system retrieves all matching customer records and LLM summarises non-sensitive information.

**Independent Test**: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "Who is Emily Johnson?"}'` returns a non-null `answer` summarising Emily Johnson's non-sensitive details, drawn only from customers.json.

### Implementation for User Story 2

- [x] T016 [US2] Implement `lookup_customers(query: str, customers: list[dict]) -> list[dict]` in `customer_lookup.py` — case-insensitive substring match against `first_name`, `last_name`, and concatenated full name; returns ALL matching customer dicts (multiple matches allowed)
- [x] T017 [US2] Update `build_prompt()` in `chat_handler.py` to format multiple customer records clearly in the LLM context — each record presented as a labelled block so the LLM can synthesise a combined answer when multiple customers share a name (depends on T012, T016)

**Checkpoint**: User Stories 1 AND 2 independently functional

---

## Phase 5: User Story 3 - Sensitive Data Refusal (Priority: P3)

**Goal**: LLM refuses requests for passwords, banking details, and precise address information with a polite explanation.

**Independent Test**: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What is Emily Johnson'\''s password?"}'` returns `answer: null` and `error` containing a polite refusal.

### Implementation for User Story 3

- [x] T018 [US3] Update system prompt in `build_prompt()` in `chat_handler.py` — add explicit sensitivity rules: MUST refuse passwords and banking details outright; for address fields MUST use judgment (city/country may be shared, street/postal code/full address MUST be refused) (depends on T012)

**Checkpoint**: Sensitive data requests are politely refused; non-sensitive location details may still be answered

---

## Phase 6: User Story 4 - Invalid or Irrelevant Question (Priority: P4)

**Goal**: LLM responds gracefully when no relevant data is found — never invents information.

**Independent Test**: `curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{"question": "What is the weather today?"}'` returns `answer: null` and `error` explaining no relevant data was found.

### Implementation for User Story 4

- [x] T019 [US4] Update system prompt in `build_prompt()` in `chat_handler.py` — add no-hallucination rule: if the provided context contains no relevant data, the LLM MUST respond gracefully explaining it found no relevant information and MUST NOT invent or guess; applies even when both product and customer lists are empty (depends on T018)

**Checkpoint**: All four user stories independently functional

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final wiring, review, and manual validation

- [x] T020 Review `build_prompt()` in `chat_handler.py` — confirm system prompt instructions are non-contradictory, cover all four user story scenarios, and produce consistent JSON-shaped responses
- [ ] T021 Manual end-to-end validation using all four curl examples in `specs/001-internal-chatbot/quickstart.md` — confirm each scenario returns a valid ChatResponse JSON matching the contracts/api.md contract

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; T002, T003, T004 are parallel
- **Foundational (Phase 2)**: Depends on Setup completion; T007 and T008 parallel
- **US1 (Phase 3)**: Depends on Phase 2 — T009 and T010 parallel; T011 depends on T009+T010; T012→T013; T014 depends on T007+T008+T010; T015 depends on T011+T013+T014+T016
- **US2 (Phase 4)**: T016 must complete before T015 (wired into /chat); T017 depends on T012+T016
- **US3 (Phase 5)**: T018 depends on T012
- **US4 (Phase 6)**: T019 depends on T018
- **Polish (Phase 7)**: Depends on all story phases complete

### User Story Dependencies

- **US1 (P1)**: Start after Phase 2 — no story dependencies
- **US2 (P2)**: T016 required before T015; otherwise can progress alongside US1
- **US3 (P3)**: Depends on T012 (build_prompt exists)
- **US4 (P4)**: Depends on T018 (US3 system prompt base)

### Parallel Opportunities

```bash
# Phase 1 parallel:
T002: Create .env.example
T003: Create data/products.json
T004: Create data/customers.json

# Phase 2 parallel:
T007: Create product_search.py loader
T008: Create customer_lookup.py loader

# Phase 3 parallel (after T008, T009 prereqs met):
T009: embed_text()
T010: build_index()
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (T009–T015)
4. **STOP and VALIDATE**: `POST /chat` with a product question → verify JSON response
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → skeleton ready
2. US1 → product questions work → demo
3. US2 → customer lookups work → demo
4. US3 → sensitive data refused → demo
5. US4 → irrelevant questions handled gracefully → demo
6. Polish → final validation

---

## Notes

- [P] = different files, no shared state dependencies — safe to run in parallel
- [USN] = maps task to user story N for traceability
- T015 has a forward dependency on T016 — implement T016 (customer lookup) before wiring /chat endpoint
- Commit after each phase checkpoint
- Manual curl validation is the acceptance gate for each user story (no automated tests per constitution)

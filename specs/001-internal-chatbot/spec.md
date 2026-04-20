# Feature Specification: Internal Support & Sales Chatbot

**Feature Branch**: `001-internal-chatbot`
**Created**: 2026-04-20
**Status**: Draft
**Input**: User description: internal assistant chatbot for support and sales staff using product and customer data

## User Scenarios

### User Story 1 - Product Question (Priority: P1)

A support or sales employee asks a question about a product (e.g., "What does this mascara do?"). The system retrieves semantically relevant products from products.json using embedding-based search and the language model answers based solely on that data.

**Why this priority**: Core use case — product knowledge is the most frequent daily need for support/sales staff.

**Independent Test**: Ask "What does [product name] do?" and verify the response describes the product accurately using only data from products.json, with a confidence score and no invented details.

**Acceptance Scenarios**:

1. **Given** a valid product question, **When** the chatbot receives it, **Then** it returns a JSON response with a non-null `answer` describing the product, `confidence` between 0 and 1, and `error` null.
2. **Given** a product question where no matching product exists, **When** the chatbot receives it, **Then** it returns `answer` null, low `confidence`, and an `error` explaining that no data was found.

---

### User Story 2 - Customer Lookup (Priority: P2)

An employee asks about a customer by first name, last name, or full name (e.g., "Who is Emily Johnson?"). The system retrieves the matching customer record from customers.json by name and the language model summarises non-sensitive information.

**Why this priority**: Customer context is essential during support calls and sales conversations.

**Independent Test**: Ask "Who is [customer name]?" and verify the response contains accurate, non-sensitive customer information drawn only from customers.json.

**Acceptance Scenarios**:

1. **Given** a customer name that exists in customers.json, **When** the chatbot receives the question, **Then** it returns a JSON response with a non-null `answer` summarising non-sensitive customer details.
2. **Given** a customer name that does not exist, **When** the chatbot receives the question, **Then** it returns `answer` null with an appropriate message indicating no record was found.

---

### User Story 3 - Sensitive Data Request (Priority: P3)

An employee (or malicious actor) asks for sensitive information such as passwords, addresses, or banking details. The language model detects the sensitivity and politely refuses, without exposing any data.

**Why this priority**: Data integrity — the system must not leak sensitive fields even if they exist in the source files.

**Independent Test**: Ask "What is Emily Johnson's password?" and verify the response refuses politely with `answer` null and an explanation in `error`.

**Acceptance Scenarios**:

1. **Given** a question requesting passwords, addresses, or banking details, **When** the chatbot receives it, **Then** the LLM returns a polite refusal with `answer` null and `error` describing why the request cannot be fulfilled.

---

### User Story 4 - Invalid or Irrelevant Question (Priority: P4)

An employee asks something outside the system's knowledge domain (e.g., "What is the weather today?"). The chatbot acknowledges it cannot answer rather than guessing.

**Why this priority**: Trust — users must not receive fabricated answers.

**Independent Test**: Ask an off-topic question and verify the response contains `answer` null and an `error` or explanation that the system has no relevant data.

**Acceptance Scenarios**:

1. **Given** an irrelevant question, **When** the chatbot receives it, **Then** it returns `answer` null, low `confidence`, and `error` indicating no relevant data is available.

---

### Edge Cases

- What happens when both products.json and customers.json return no results? → The LLM is still called with empty context and MUST respond gracefully explaining that no relevant information was found.
- How does the system handle a question that is partially sensitive (e.g., "What city does Emily Johnson live in?")? → The LLM uses judgment: non-specific location details (city, country) may be answered; precise address details (street, postal code, full address) MUST be refused.
- What if the query matches multiple customers with the same name? → All matching records are returned to the LLM; the LLM synthesises a combined answer.

## Requirements

### Functional Requirements

- **FR-001**: System MUST accept a natural-language question as input and return a structured JSON response.
- **FR-002**: System MUST retrieve the top 3 semantically relevant products from products.json using embedding-based similarity search.
- **FR-003**: System MUST retrieve customer records from customers.json using exact or partial name matching (first name, last name, or full name). If multiple records match, ALL matching records MUST be returned to the language model.
- **FR-004**: System MUST send both retrieved product data and customer data to the language model in a single call. The LLM MUST always be called, even when both data sources return no results; in that case it MUST respond gracefully explaining that no relevant information was found.
- **FR-005**: System MUST return responses in JSON with exactly three fields: `answer` (string or null), `confidence` (number 0–1), `error` (string or null).
- **FR-006**: Language model MUST refuse requests for sensitive data (passwords, precise address details, banking details) with a polite explanation; no other security layer is required. For address-related questions, the LLM MUST use judgment — non-specific location details (city, country) MAY be answered; precise details (street, postal code, full address) MUST be refused.
- **FR-007**: Language model MUST NOT invent or guess information; if insufficient data is available it MUST say so.
- **FR-008**: Language model MUST base its answer solely on the data provided to it in the single LLM call.

### Key Entities

- **Product**: An item in the product catalogue with descriptive attributes (name, description, category, etc.).
- **Customer**: A person record with identifying and transactional attributes; some fields are sensitive.
- **ChatRequest**: The incoming question from the employee.
- **ChatResponse**: The structured JSON response (`answer`, `confidence`, `error`).

## Success Criteria

### Measurable Outcomes

- **SC-001**: Product questions return accurate answers based exclusively on products.json data with no fabricated details.
- **SC-002**: Customer lookups return correct non-sensitive information when the customer exists in customers.json.
- **SC-003**: Requests for sensitive data are refused 100% of the time via the language model's response.
- **SC-004**: Questions with no matching data result in a clear "no data available" response rather than a guess.
- **SC-005**: Every response conforms to the defined JSON schema (`answer`, `confidence`, `error`).

## Clarifications

### Session 2026-04-20

- Q: When multiple customers match the same name, what should the system return? → A: Return all matching customer records to the LLM; let it synthesise the answer.
- Q: How should the system handle partially sensitive requests (e.g., "What city does Emily Johnson live in?")? → A: LLM judgment — non-specific location details (city, country) may be answered; precise address details (street, postal code, full address) must be refused.
- Q: How many products should semantic search return per query (top-K)? → A: 3.
- Q: When both data sources return no results, should the LLM still be called? → A: Yes — the LLM is always called and responds gracefully explaining no relevant information was found.

## Assumptions

- The system is a backend service only; no frontend UI is in scope.
- products.json and customers.json are static files available at runtime; no database is required.
- Embeddings for products are pre-computed or computed at startup; no streaming pipeline is needed.
- The language model used is an OpenAI-compatible model accessible via API key in environment variables.
- No authentication or access control is required beyond the LLM's sensitivity refusal behaviour.
- The system targets a small internal team; high concurrency is not a requirement.
- "Sensitive fields" include at minimum: passwords, physical addresses, banking/payment details.

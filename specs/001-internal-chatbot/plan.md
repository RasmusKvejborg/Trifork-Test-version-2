# Implementation Plan: Internal Support & Sales Chatbot

**Branch**: `001-internal-chatbot` | **Date**: 2026-04-20 | **Spec**: specs/001-internal-chatbot/spec.md
**Input**: Feature specification from `specs/001-internal-chatbot/spec.md`

## Summary

Build a FastAPI backend that accepts natural-language questions from support and sales staff, retrieves
relevant products via embedding-based semantic search and customers via name lookup, and passes both
datasets to a language model in a single call to generate a structured JSON answer.

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: FastAPI, uvicorn[standard], openai, numpy, python-dotenv, pydantic
**Storage**: Flat JSON files (products.json, customers.json) + in-memory numpy embedding index
**Testing**: N/A — automated tests are FORBIDDEN per constitution
**Target Platform**: Linux server / local development
**Project Type**: web-service
**Performance Goals**: Internal tool; response under 5 seconds per request; low concurrency
**Constraints**: Single LLM call per request; no database; no frontend
**Scale/Scope**: ~10 concurrent internal users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle               | Status | Notes                                                                 |
|-------------------------|--------|-----------------------------------------------------------------------|
| I. Clarity Over Cleverness | ✅ PASS | Modules named by responsibility: product_search, customer_lookup, chat_handler |
| II. Single Responsibility | ✅ PASS | Embedding search, name lookup, and LLM call are separate modules      |
| III. Simplicity (YAGNI)  | ✅ PASS | Flat files, no DB, no auth, no streaming pipeline                     |
| IV. No Dead Code         | ✅ PASS | Enforced during implementation review                                 |
| No-Testing Policy        | ✅ PASS | No test files or test dependencies                                    |

**Gate result**: PASS — proceed to implementation.

## Project Structure

### Documentation (this feature)

```text
specs/001-internal-chatbot/
├── plan.md              # This file
├── spec.md              # Feature specification
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── api.md           # REST API contract
└── tasks.md             # Phase 2 output (/speckit-tasks)
```

### Source Code (repository root)

```text
main.py                  # FastAPI app entry point, /chat and /health endpoints
product_search.py        # Load products.json, compute embeddings, semantic search
customer_lookup.py       # Load customers.json, name-based lookup
chat_handler.py          # Build LLM prompt, call OpenAI, parse response
models.py                # Pydantic models: ChatRequest, ChatResponse
data/
├── products.json        # Product catalogue (provided)
└── customers.json       # Customer records (provided)
.env                     # OPENAI_API_KEY (not committed)
requirements.txt         # Pinned dependencies
```

**Structure Decision**: Single flat package at repository root. Scope is one endpoint with three
collaborating modules. A `src/` layout would add indirection without benefit.

## Complexity Tracking

> No violations — complexity tracking not required.

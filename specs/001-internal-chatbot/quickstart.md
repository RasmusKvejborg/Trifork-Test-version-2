# Quickstart: Internal Support & Sales Chatbot

## Prerequisites

- Python 3.11+
- OpenAI API key

## Setup

```bash
pip install fastapi "uvicorn[standard]" openai numpy python-dotenv pydantic
```

Create a `.env` file at the repository root:

```
OPENAI_API_KEY=sk-...
```

Place your data files at the repository root:

```
products.json
customers.json
```

## Run

```bash
uvicorn main:app --reload
```

The API is available at `http://localhost:8000`.

## Try It

**Product question**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What does the volumizing mascara do?"}'
```

**Customer lookup**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Who is Emily Johnson?"}'
```

**Sensitive data (refused)**:
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Emily Johnson'\''s password?"}'
```

**Health check**:
```bash
curl http://localhost:8000/health
```

## Expected Response Shape

```json
{
  "answer": "...",
  "confidence": 0.85,
  "error": null
}
```

# API Contract: Internal Support & Sales Chatbot

## Base URL

`http://localhost:8000`

---

## POST /chat

Send a natural-language question and receive a structured answer.

### Request

```
POST /chat
Content-Type: application/json
```

**Body**:

```json
{
  "question": "What does the volumizing mascara do?"
}
```

| Field    | Type   | Required | Description                        |
|----------|--------|----------|------------------------------------|
| question | string | Yes      | The employee's natural-language question |

### Response

**Status**: `200 OK` (always — errors are returned in the body, not as HTTP error codes)

```json
{
  "answer": "The volumizing mascara adds thickness and length to lashes...",
  "confidence": 0.92,
  "error": null
}
```

| Field      | Type          | Description                                               |
|------------|---------------|-----------------------------------------------------------|
| answer     | string or null | The chatbot's answer; null if no answer could be generated |
| confidence | number        | Model-assigned confidence score between 0.0 and 1.0       |
| error      | string or null | Error message; null on success                            |

### Example Scenarios

**Product question — answer found**:
```json
{ "answer": "This mascara...", "confidence": 0.88, "error": null }
```

**Customer lookup — customer not found**:
```json
{ "answer": null, "confidence": 0.0, "error": "No customer matching 'John Doe' was found." }
```

**Sensitive data request — refused by LLM**:
```json
{ "answer": null, "confidence": 1.0, "error": "I cannot share sensitive personal information such as passwords or banking details." }
```

**Irrelevant question — no data**:
```json
{ "answer": null, "confidence": 0.0, "error": "I don't have information to answer that question." }
```

---

## GET /health

Basic liveness check.

### Response

**Status**: `200 OK`

```json
{ "status": "ok" }
```

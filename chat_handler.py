import json

from openai import OpenAI

from models import ChatResponse

LLM_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = """You are an internal assistant for support and sales staff. You answer questions
using only the product and customer data provided below. You MUST NOT invent, guess, or extrapolate
any information beyond what is explicitly present in the provided data.

LANGUAGE RULE: Always respond in the same language as the question. If the question is in Danish, answer in Danish. If in English, answer in English.

SENSITIVE DATA RULES — enforce these strictly:
- NEVER reveal passwords or password hashes under any circumstances.
- NEVER reveal bank account numbers or any payment/financial details.
- For address fields: you MAY share general information, (e.g. the city a person lives in) but not precise details (e.g. street name or a full address string).
- If asked for sensitive data, refuse politely and explain you cannot share that information.

NO-DATA RULE:
- If the provided context contains no relevant information to answer the question,
  respond gracefully explaining that you could not find any relevant information.
  Do not attempt to answer from general knowledge.

RESPONSE FORMAT — you MUST always respond with valid JSON containing exactly these three fields:
{
  "answer": "<your answer as a string, or null if you cannot answer>",
  "confidence": <a number between 0.0 and 1.0 reflecting your confidence>,
  "error": "<a description of why you cannot answer, or null if you answered successfully>"
}"""


def build_prompt(
    question: str, products: list[dict], customers: list[dict]
) -> list[dict]:
    context_parts = []

    if products:
        context_parts.append(f"## Relevant Products\n\n{json.dumps(products, ensure_ascii=False, indent=2)}")
    else:
        context_parts.append("## Relevant Products\n\nNo products found.")

    if customers:
        context_parts.append(f"## Matching Customers\n\n{json.dumps(customers, ensure_ascii=False, indent=2)}")
    else:
        context_parts.append("## Matching Customers\n\nNo customers found.")

    user_message = "\n\n".join(context_parts) + f"\n\n## Question\n\n{question}"

    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]


def call_llm(
    question: str,
    products: list[dict],
    customers: list[dict],
    client: OpenAI,
) -> ChatResponse:
    print(f"Question: ", question)

    print(f"Products:")
    for p in products:
        print(p)
    print(f"Customers:")    
    for c in customers:
        print(c)

    messages = build_prompt(question, products, customers)
    # print(messages)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=messages,
        response_format={"type": "json_object"},
    )
    raw = json.loads(response.choices[0].message.content)
    return ChatResponse(
        answer=raw.get("answer"),
        confidence=float(raw.get("confidence", 0.0)),
        error=raw.get("error"),
    )

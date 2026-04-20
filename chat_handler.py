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
- For address fields: you MAY share general location information (city, country, region).
  You MUST NOT share precise address details (street name, house number, postal/ZIP code,
  or a full address string).
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
        product_text = "\n\n".join(
            f"Product ID: {p.get('id', 'N/A')}\n"
            f"Name: {p.get('name', 'N/A')}\n"
            f"Category: {p.get('category', 'N/A')}\n"
            f"Description: {p.get('description', 'N/A')}"
            for p in products
        )
        context_parts.append(f"## Relevant Products\n\n{product_text}")
    else:
        context_parts.append("## Relevant Products\n\nNo products found.")

    if customers:
        customer_text = "\n\n".join(
            f"--- Customer Record {i + 1} ---\n"
            + "\n".join(f"{k}: {v}" for k, v in c.items())
            for i, c in enumerate(customers)
        )
        context_parts.append(f"## Matching Customers\n\n{customer_text}")
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
        print(f"  - {p.get('id')} {p.get('name')}", flush=True)
    print(f"Customers:")    
    for c in customers:
        print(f"  - {c.get('id')} {c.get('first_name')} {c.get('last_name')}", flush=True)

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

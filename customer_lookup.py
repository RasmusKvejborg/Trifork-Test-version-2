import json


def load_customers(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def lookup_customers(query: str, customers: list[dict]) -> list[dict]:
    query_lower = query.lower()
    matches = []
    for customer in customers:
        first = customer.get("first_name", "").lower()
        last = customer.get("last_name", "").lower()
        full = f"{first} {last}"
        if query_lower in first or query_lower in last or query_lower in full:
            matches.append(customer)
    return matches

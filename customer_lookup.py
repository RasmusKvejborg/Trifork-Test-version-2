import json
import re


def load_customers(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def lookup_customers(query: str, customers: list[dict]) -> list[dict]:
    tokens = set(re.findall(r"[a-zæøå]+", query.lower()))
    matches = []
    for customer in customers:
        first = customer.get("first_name", "").lower()
        last = customer.get("last_name", "").lower()
        if first in tokens or last in tokens:
            matches.append(customer)
    return matches

import json
import re


def load_customers(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)["customers"]


def lookup_customers(query: str, customers: list[dict], max_results: int = 5) -> list[dict]:
    tokens = set(re.findall(r"[a-zæøå]+", query.lower()))
    matches = []
    for customer in customers:
        first = customer.get("firstName", "").lower()
        last = customer.get("lastName", "").lower()
        if first in tokens or last in tokens:
            matches.append(customer)
            if len(matches) == max_results:
                break
    return matches

import json

import numpy as np
from openai import OpenAI

EMBEDDING_MODEL = "text-embedding-3-small"


def load_products(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)["products"]


def embed_text(text: str, client: OpenAI) -> list[float]:
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=text)
    return response.data[0].embedding


def build_index(
    products: list[dict], client: OpenAI
) -> tuple[np.ndarray, list[dict]]:
    texts = [p["description"] for p in products]
    response = client.embeddings.create(model=EMBEDDING_MODEL, input=texts)
    embeddings = [e.embedding for e in response.data]
    return np.array(embeddings, dtype=np.float32), products


def search_products(
    query: str,
    index: np.ndarray,
    products: list[dict],
    client: OpenAI,
    top_k: int = 3,
) -> list[dict]:
    query_embedding = np.array(embed_text(query, client), dtype=np.float32)
    norms = np.linalg.norm(index, axis=1) * np.linalg.norm(query_embedding)
    norms = np.where(norms == 0, 1e-10, norms)
    similarities = np.dot(index, query_embedding) / norms
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [products[i] for i in top_indices]

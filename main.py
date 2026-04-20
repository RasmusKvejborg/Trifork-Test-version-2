from contextlib import asynccontextmanager

import numpy as np
from dotenv import load_dotenv
from fastapi import FastAPI
from openai import OpenAI

from chat_handler import call_llm
from customer_lookup import load_customers, lookup_customers
from models import ChatRequest, ChatResponse
from product_search import build_index, load_products, search_products

load_dotenv()

PRODUCTS_PATH = "data/products.json"
CUSTOMERS_PATH = "data/customers.json"


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = OpenAI()
    products = load_products(PRODUCTS_PATH)
    embedding_index, indexed_products = build_index(products, client)
    customers = load_customers(CUSTOMERS_PATH)

    app.state.client = client
    app.state.embedding_index = embedding_index
    app.state.indexed_products = indexed_products
    app.state.customers = customers

    yield


app = FastAPI(lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    client: OpenAI = app.state.client
    embedding_index: np.ndarray = app.state.embedding_index
    indexed_products: list[dict] = app.state.indexed_products
    customers: list[dict] = app.state.customers

    relevant_products = search_products(
        request.question, embedding_index, indexed_products, client
    )
    matching_customers = lookup_customers(request.question, customers)

    return call_llm(request.question, relevant_products, matching_customers, client)

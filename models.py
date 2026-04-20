from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str | None = None
    confidence: float = Field(ge=0.0, le=1.0)
    error: str | None = None

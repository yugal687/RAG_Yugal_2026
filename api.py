from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from llm import generate_answer, load_model
from pinecone_db import get_index
from prompt_builder import build_prompt
from retriever import retrieve


index = None


class AskRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        max_length=500
    )


class SourceResponse(BaseModel):
    source: str
    chunk_number: int
    score: float
    text: str


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Load the language model and Pinecone index once when FastAPI starts.
    """

    global index

    print("Starting RAG API...")
    load_model()
    index = get_index()
    print("RAG API is ready.")

    yield

    print("Stopping RAG API...")


app = FastAPI(
    title="RAG Assistant API",
    description="A local RAG API using Pinecone and Llama 3.2.",
    version="1.0.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"]
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "message": "RAG Assistant API is running."
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "healthy",
        "model": "meta-llama/Llama-3.2-3B-Instruct"
    }


@app.post("/ask", response_model=AskResponse)
def ask_question(request: AskRequest) -> AskResponse:
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:
        if index is None:
            raise RuntimeError("Pinecone index is not initialized.")

        retrieval_results: dict[str, Any] = retrieve(
            index,
            question
        )

        matches = retrieval_results.get("matches", [])

        if not matches:
            return AskResponse(
                question=question,
                answer="I don't have enough information to answer that.",
                sources=[]
            )

        prompt = build_prompt(
            question=question,
            results=retrieval_results
        )

        answer = generate_answer(
            prompt=prompt,
            max_new_tokens=128
        )

        sources = []

        for match in matches:
            metadata = match.get("metadata", {})

            sources.append(
                SourceResponse(
                    source=str(
                        metadata.get("source", "Unknown source")
                    ),
                    chunk_number=int(
                        metadata.get("chunk_number", -1)
                    ),
                    score=float(
                        match.get("score", 0.0)
                    ),
                    text=str(
                        metadata.get("text", "")
                    )
                )
            )

        return AskResponse(
            question=question,
            answer=answer,
            sources=sources
        )

    except Exception as error:
        import traceback

        traceback.print_exc()

        raise HTTPException(
            status_code=500,
            detail=str(error)
        ) from error
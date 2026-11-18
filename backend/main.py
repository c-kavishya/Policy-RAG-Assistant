from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from rag import retrieve_chunks, generate_answer

app = FastAPI(title="Policy RAG Assistant API")


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def health_check():
    return {"status": "running", "message": "Policy RAG API is ready"}


@app.post("/ask")
def ask_policy(request: QuestionRequest):
    try:
        chunks = retrieve_chunks(request.question) 

        answer = generate_answer(request.question, chunks)

        return {"answer": answer, "sources": chunks}
    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
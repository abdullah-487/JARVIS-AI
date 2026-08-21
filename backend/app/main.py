from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.agent import ask_jarvis
from pydantic import BaseModel

app = FastAPI(title="JARVIS AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    mode: str = "auto"

@app.get("/")
def home():
    return {"status": "JARVIS ONLINE"}

@app.post("/ask")
def ask(request: AskRequest):
    try:
        return ask_jarvis(request.question, request.mode)
    except Exception as e:
        return {"error": str(e)}

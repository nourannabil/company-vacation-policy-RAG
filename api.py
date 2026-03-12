from main import query_documents
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins. Use specific domains for better security.
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"]   # Allow all headers
)


class Question(BaseModel):
    question : str
    
    
@app.post("/ask")
def ask_question(q: Question):

    answer = query_documents(q.question)

    return {
        "question": q.question,
        "answer": answer
    }
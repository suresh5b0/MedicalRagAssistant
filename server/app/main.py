from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi import UploadFile, File

from pydantic import BaseModel

import shutil
import os
from pathlib import Path

from server.app.agent import create_agent

from .rag import create_chain

app = FastAPI(
    title="Medical AI Assistant"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = create_agent()

qa_chain = create_chain()

class QueryRequest(BaseModel):
    question: str

@app.get("/")
def home():

    return {
        "message": "Medical AI Assistant Running"
    }

@app.post("/ask")
def ask_question(request: QueryRequest):

    response = qa_chain.invoke({
        "query": request.question
    })

    return {
        "question": request.question,
        "answer": response["result"],
        "sources": [
            doc.metadata
            for doc in response["source_documents"]
        ]
    }


class Query(BaseModel):
    question: str


@app.post("/agentask")
def ask(q: Query):

    response = agent.run(q.question)

    return {
        "question": q.question,
        "answer": response
    }



@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    file_path = f"data/medical_docs/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    return {
        "message": f"{file.filename} uploaded"
    }
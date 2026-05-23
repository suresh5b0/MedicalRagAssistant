from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi import UploadFile, File

from pydantic import BaseModel

import shutil
import os
from pathlib import Path

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

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):
    try:
        # Get the directory where this file is located
        app_dir = Path(__file__).parent.parent
        upload_dir = app_dir / "data" / "medical_docs"
        
        # Create directory if it doesn't exist
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / file.filename
        
        # Save the file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )
        
        return {
            "message": f"{file.filename} uploaded successfully"
        }
    except Exception as e:
        return {
            "message": f"Error uploading {file.filename}: {str(e)}"
        }
#!/usr/bin/env python3
"""Initialize vector database with sample medical data"""

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
import os

def init_vectordb():
    # Create sample medical documents
    sample_docs = [
        Document(
            page_content="Hypertension is a condition characterized by high blood pressure. Common treatments include ACE inhibitors, beta-blockers, and diuretics.",
            metadata={"source": "sample_medical.txt", "page": 1}
        ),
        Document(
            page_content="Diabetes mellitus is a metabolic disorder affecting blood glucose regulation. Type 1 and Type 2 are the most common forms.",
            metadata={"source": "sample_medical.txt", "page": 2}
        ),
        Document(
            page_content="Pneumonia is an infection causing inflammation of the lungs' air sacs. Symptoms include cough, fever, and difficulty breathing.",
            metadata={"source": "sample_medical.txt", "page": 3}
        ),
        Document(
            page_content="Cardiac arrhythmia refers to irregular heartbeat. ECG monitoring is essential for diagnosis and management.",
            metadata={"source": "sample_medical.txt", "page": 4}
        ),
    ]

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector store
    vectorstore = FAISS.from_documents(
        sample_docs,
        embeddings
    )

    # Save to disk
    os.makedirs("vectorstore/db_faiss", exist_ok=True)
    vectorstore.save_local("vectorstore/db_faiss")
    print("[OK] Vector database initialized successfully")

if __name__ == "__main__":
    init_vectordb()

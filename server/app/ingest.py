from langchain_community.document_loaders import PyPDFDirectoryLoader

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS

from langchain_huggingface import HuggingFaceEmbeddings

from .config import (
    DATA_PATH,
    DB_FAISS_PATH,
    EMBEDDING_MODEL
)

def create_vector_db():

    print("Loading PDFs...")

    loader = PyPDFDirectoryLoader(DATA_PATH)

    documents = loader.load()

    print(f"Loaded {len(documents)} pages")

    print("Splitting documents...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_documents(documents)

    print(f"Created {len(chunks)} chunks")

    print("Loading embeddings model...")

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    print("Creating FAISS database...")

    db = FAISS.from_documents(
        chunks,
        embeddings
    )

    db.save_local(DB_FAISS_PATH)

    print("FAISS DB Saved Successfully")

if __name__ == "__main__":
    create_vector_db()
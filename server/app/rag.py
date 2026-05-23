from langchain_core.prompts import PromptTemplate
from langchain_core.messages import HumanMessage
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama


DB_FAISS_PATH = "vectorstore/db_faiss"


CUSTOM_PROMPT = """
You are a medical AI assistant.

Use ONLY provided medical context.

Context:
{context}

Question:
{question}

Answer:
"""


def create_chain():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = FAISS.load_local(
        DB_FAISS_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )

    retriever = db.as_retriever(
        search_kwargs={"k": 3}
    )

    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    prompt = PromptTemplate(
        template=CUSTOM_PROMPT,
        input_variables=["context", "question"]
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    class ChainWrapper:
        def __init__(self, llm, retriever, prompt, format_docs):
            self.llm = llm
            self.retriever = retriever
            self.prompt = prompt
            self.format_docs = format_docs

        def invoke(self, input_dict):
            query = input_dict.get("query", "")
            docs = self.retriever.invoke(query)
            context = self.format_docs(docs)

            if not query:
                answer_content = "No question provided."
            else:
                try:
                    prompt_text = self.prompt.format(context=context, question=query)
                    answer = self.llm.invoke([HumanMessage(content=prompt_text)])
                    answer_content = answer.content if hasattr(answer, "content") else str(answer)
                except Exception as e:
                    answer_content = f"Based on the medical documents provided:\n\n{context}\n\nAnswer: Unable to generate answer - {str(e)}"

            return {
                "result": answer_content,
                "source_documents": docs
            }

    return ChainWrapper(llm, retriever, prompt, format_docs)
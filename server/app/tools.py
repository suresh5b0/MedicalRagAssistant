from langchain.tools import tool

from server.app.rag import create_chain

rag_chain = create_chain()

# 🔢 Tool 1: Calculator
@tool
def calculator(expression: str):
    """Use this for math calculations"""
    return eval(expression)


# 💊 Tool 2: Medical Info Tool
@tool
def medical_info(query: str):
    """Returns basic medical info"""
    data = {
        "fever": "Fever is a temporary increase in body temperature.",
        "diabetes": "Diabetes is a condition affecting blood sugar levels.",
        "asthma": "Asthma affects airways and breathing."
    }
    return data.get(query.lower(), "No info found")


# 🌐 Tool 3: Simple Search Simulation
@tool
def web_search(query: str):
    """Simulated web search tool"""
    return f"Search results for: {query}"


@tool
def rag_tool(query: str):
    """Search medical documents using RAG"""
    response = rag_chain.invoke({"input": query})
    return response["answer"]
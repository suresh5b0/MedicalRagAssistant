from langchain_ollama import ChatOllama
from langchain.agents import initialize_agent, AgentType
from app.tools import calculator, medical_info, web_search


def create_agent():

    # 🦙 LLM
    llm = ChatOllama(
        model="llama3.2",
        temperature=0
    )

    # 🧰 Tools list
    tools = [
        calculator,
        medical_info,
        web_search
    ]

    # 🧠 Create Agent
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    return agent
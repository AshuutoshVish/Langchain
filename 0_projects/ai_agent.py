import os
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

def get_response_from_ai_agent(llm_id, provider, query, allow_search, system_prompt):
    provider = provider.strip().capitalize()

    if provider == "Groq":
        llm = ChatGroq(model=llm_id)
    elif provider == "Gemini":
        llm = ChatGoogleGenerativeAI(model=llm_id)
    else:
        raise ValueError(f"Unsupported provider '{provider}'. Use 'Groq' or 'Gemini'.")

    tools = [TavilySearchResults(max_results=2)] if allow_search else []

    agent = create_react_agent(
        model=llm,
        tools=tools,
        system_message=system_prompt  # Correct parameter name
    )

    state = {"messages": query}
    response = agent.invoke(state)
    messages = response.get("messages", [])
    ai_messages = [msg.content for msg in messages if isinstance(msg, AIMessage)]
    return ai_messages[-1] if ai_messages else "No AI response."

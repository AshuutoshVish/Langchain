import streamlit as st
import requests

st.set_page_config(page_title="LangGraph Agent UI", layout="centered")
st.title("AI Agent Chatbot")
st.write("Create and interact with an AI agent powered by LangGraph!")

system_prompt = st.text_area("Define your AI Agent:", height=75, placeholder="Type your system prompt here...")

# Model names
MODEL_NAMES_GROQ = ["llama3-70b-8192"]
MODEL_NAMES_GEMINI = ["gemini-2.0-flash"]

# Provider selection
provider = st.radio("Select Provider:", ("Groq", "Gemini"))
selected_model = st.selectbox(
    "Select Model:",
    MODEL_NAMES_GROQ if provider == "Groq" else MODEL_NAMES_GEMINI
)

# Web search toggle
allow_web_search = st.checkbox("Allow Web Search")

# User query
user_query = st.text_area("Enter your query here:", height=150, placeholder="Ask anything you want!")

API_URL = "http://127.0.0.1:8888/chat"

if st.button("Ask Agent!"):
    if user_query.strip():
        payload = {
            "model_name": selected_model,
            "model_provider": provider,
            "system_prompt": system_prompt,
            "messages": [user_query],
            "allow_search": allow_web_search
        }

        response = requests.post(API_URL, json=payload)

        if response.status_code == 200:
            response_data = response.json()
            if "error" in response_data:
                st.error(response_data["error"])
            else:
                st.subheader(" Agent Response")
                st.markdown(response_data["response"])
        else:
            st.error("Failed to get a response from the backend.")

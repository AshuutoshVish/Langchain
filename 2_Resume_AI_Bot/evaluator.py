from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.2, google_api_key=api_key)

prompt_template = PromptTemplate(
    input_variables=["question", "answer"],
    template="""
You are an AI interview assistant.

Evaluate the following candidate response based on the question. 
Score it from 1 to 10 based on:
- Correctness
- Clarity
- Depth

Also, give brief feedback.

Question: {question}
Answer: {answer}

Respond in this format:
Score: <score>/10
Feedback: <short_feedback>
"""
)

def evaluate_answer(question, answer):
    chain = LLMChain(prompt=prompt_template, llm=llm)
    return chain.run({"question": question, "answer": answer}).strip()

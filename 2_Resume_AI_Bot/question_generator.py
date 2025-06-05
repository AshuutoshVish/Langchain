from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from resume_parser import extract_resume_info
import os

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.5, google_api_key=api_key)

question_prompt = PromptTemplate(
    input_variables=["info"],
    template="""
You are a technical interviewer.

Based on the following extracted resume details, generate:
- 5 technical interview questions relevant to the candidate’s skills and projects
- 2 behavioral interview questions that test communication, adaptability, and team fit

Resume Info:
{info}

Respond with clearly numbered questions.
"""
)

def generate_questions(resume_text: str):
    info = extract_resume_info(resume_text)
    chain = LLMChain(prompt=question_prompt, llm=llm)
    response = chain.run({"info": info})
    return [q.strip() for q in response.strip().split("\n") if q.strip()]

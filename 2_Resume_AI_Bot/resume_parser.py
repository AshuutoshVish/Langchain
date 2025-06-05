import os
import pdfplumber
import docx2txt
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash', temperature=0.2, google_api_key=api_key)

info_template = PromptTemplate(
    input_variables=["resume_text"],
    template="""
You are a helpful resume parsing assistant.

Extract the following from the resume:
1. Key Skills
2. Projects (with titles and summaries if available)
3. Job Titles or Designations
4. Work Experience Summary (company names, roles, durations)
5. Suggested Target Role (based on above data)

Resume:
{resume_text}

Respond in structured bullet points grouped by section.
"""
)

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        return " ".join([page.extract_text() or "" for page in pdf.pages])

def extract_text_from_docx(file_path):
    return docx2txt.process(file_path)

def parse_resume(file_path):
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

def extract_resume_info(resume_text):
    chain = LLMChain(prompt=info_template, llm=llm)
    return chain.run({"resume_text": resume_text}).strip()

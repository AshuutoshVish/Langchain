from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
parser = StrOutputParser()
prompt = PromptTemplate(template="Write a joke about {topic}", input_variables=['topic'])
prompt_explain=PromptTemplate(template = "Explain the following joke - {text}", input_variables=['text'])
chain = RunnableSequence(prompt, model, parser, prompt_explain, model, parser)
print(chain.invoke({"topic" : "AI"}))
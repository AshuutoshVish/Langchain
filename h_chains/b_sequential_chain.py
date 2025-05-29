from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
prompt1 = PromptTemplate(template= 'Generate a detailed report on {topic}', input_variables=['topic'])
prompt2 = PromptTemplate(template= 'Generate a 5 line pointer summary on {text}', input_variables=['text'])
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
parser = StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser
result = chain.invoke({'topic' : 'AI'})
chain.get_graph().print_ascii() #pip install grandalf
print(result)
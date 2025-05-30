from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence, RunnableParallel
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
parser = StrOutputParser()
prompt = PromptTemplate(template="Generate a tweet about {topic}", input_variables=['topic'])
prompt2 = PromptTemplate(template="Generate a linkedIn post about {topic}", input_variables=['topic'])

parallel_chain = RunnableParallel({"tweet" : RunnableSequence(prompt, model, parser),
                                   "linkedIn" : RunnableSequence(prompt2, model, parser)})
result = parallel_chain.invoke({"topic": "AI"})
print(result)
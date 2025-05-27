from langchain_openai import openAI
from dotenv import load_dotenv

load_dotenv()
llm=openAI(model='gpt-3.5-turbo-instruct')

result = llm.invoke("what is the capital of Uttare Pradesh")
print(result)
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv

model = ChatOpenAI(model='gpt-4')
result = model.invoke("What is the capital of Indi?")
# print(result) #it will give some information about tokens
print(result.content)
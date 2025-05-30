from langchain_community.document_loaders import TextLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

prompt = PromptTemplate(
    template="Write a summary for the following poem \n {poem}", 
    input_variables=["poem"]
)

parser = StrOutputParser()

loader = TextLoader('ai_poem.txt', encoding='utf-8')

docs = loader.load()
print(type(docs))
print(len(docs))
print(docs[0].metadata) #ontents detail or title or name of document
# print(docs[0].page_content) #Contain the inside of doc
# print(docs[0])
# print(docs)

chain = prompt | model | parser

print(chain.invoke({"poem" : docs[0].page_content}))
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
parser = StrOutputParser()
prompt = PromptTemplate(template='Answer the following question \n {question} from the following text \n {text}',
                        input_variables=['question', 'text'])

# url = 'https://www.flipkart.com/apple-macbook-air-m2-16-gb-256-gb-ssd-macos-sequoia-mc7x4hn-a/p/itmdc5308fa78421'
url = 'https://www.myntra.com/wallets/contacts/contacts-men-beige-leather-wallets-with-rfid/17257336/buy'

loader = WebBaseLoader(url)
docs = loader.load()
chain = prompt | model | parser

print(chain.invoke({'question':'Write a short note about the product', 'text':docs[0].page_content}))
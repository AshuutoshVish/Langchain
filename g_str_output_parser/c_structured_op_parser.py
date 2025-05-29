# "It Doesn't provide Data Validation" 
# Only we can tell in whch format data is needed 
# We have to manually do so it will be removed in pydantic

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')

schema = [ResponseSchema(name='fact_1', description='Fact 1 about the Topic'),
          ResponseSchema(name='fact_2', description='Fact 2 about the Topic'),
          ResponseSchema(name='fact_3', description='Fact 3 about the Topic'),
          ResponseSchema(name='fact_4', description='Fact 4 about the Topic'),
          ResponseSchema(name='fact_5', description='Fact 5 about the Topic'),
          ]

parser = StructuredOutputParser.from_response_schemas(schema)

template = PromptTemplate(template= "Give 5 facts about {topic} \n {format_instruction}",
                          input_variables=['topic'],
                          partial_variables={'format_instruction':parser.get_format_instructions()}
                          )

#Chain
chain = template | model | parser
result = chain.invoke({'topic':'Gen AI'})
print(result)

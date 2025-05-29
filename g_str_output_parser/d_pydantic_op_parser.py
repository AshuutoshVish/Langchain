from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
class Person(BaseModel):
    name :  str = Field(description= "Name of person")
    age : int = Field(gt=18, description= "Age of the person")
    gender : str = Field(description= "Gender of the person")
    city : str = Field(description= "Name of the city of the person belongs")

parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(template="Generate the name, age, gender, city of the fictional {place} person \n{format_instruction}",
                          input_variables=['place'],
                          partial_variables={'format_instruction' : parser.get_format_instructions()}
                          )

# # # We can make a chain of all these
# prompt = template.invoke({'place':'india'})
# # print(prompt)
# result = model.invoke(prompt)
# final_result = parser.parse(result.content)
# print(final_result)

chain = template | model | parser
final_result = chain.invoke({'place' : 'india'})
print(final_result)
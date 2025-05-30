from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
class Feedback(BaseModel):
    sentiment : Literal['positive', 'negative'] = Field(description="Give the sentiment of the feedback")

feedback_parser = PydanticOutputParser(pydantic_object=Feedback)
str_parser = StrOutputParser()

classifier_prompt  = PromptTemplate(template= "Classify the sentiment of the following feedback text into positive or negative \n {feedback} \n {format_instructions}",
                         input_variables=['feedback'],
                         partial_variables={'format_instructions': feedback_parser.get_format_instructions()})

classifier_chain = classifier_prompt | model | feedback_parser


positive_prompt = PromptTemplate(template=("You are a customer support assistant. Respond warmly and appreciatively to the following positive customer feedback:\n"
                                           "\"{feedback}\"\n\n"
                                           "Your response should be professional and enthusiastic."),
                                           input_variables=['feedback'])

negative_prompt = PromptTemplate(template=("You are a customer support assistant. Respond professionally and empathetically to the following negative customer feedback:\n"
                                           "\"{feedback}\"\n\n"
                                           "Your response should be brief, sincere, and helpful."),
                                           input_variables=['feedback'])

branch_chain = RunnableBranch(
    (lambda x : x.sentiment=='positive', positive_prompt | model | str_parser),
    (lambda x : x.sentiment=='negative', negative_prompt | model | str_parser),
    RunnableLambda(lambda x: "Could not find sentiment")
)

chain = classifier_chain | branch_chain
result = chain.invoke({'feedback': "The product was good and useful after week of use"})
print(result)

chain.get_graph().print_ascii()
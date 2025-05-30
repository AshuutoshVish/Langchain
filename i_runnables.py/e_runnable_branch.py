from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence, RunnableLambda, RunnablePassthrough, RunnableParallel, RunnableBranch
from dotenv import load_dotenv

load_dotenv()

model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
parser = StrOutputParser()
prompt = PromptTemplate(template='Write a detailed report on {topic}', input_variables=['topic'])
prompt2 = PromptTemplate(template="Summarize the following text \n {text}", input_variables=["text"])

report_gen_chain = prompt | model | parser

branch_chain = RunnableBranch((lambda x : len(x.split()) > 500, RunnableSequence(prompt2, model, parser)),
                              RunnablePassthrough()
                              )

final_chain = report_gen_chain | branch_chain

result = final_chain.invoke({'topic':'AI vs ML'})
print(result)
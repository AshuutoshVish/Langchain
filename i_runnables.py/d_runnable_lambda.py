from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableSequence, RunnableParallel, RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv

load_dotenv()
model = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
parser = StrOutputParser()
prompt = PromptTemplate(template='Write a joke about {topic}', input_variables=['topic'])

def word_count(text):
    return len(text.split())

joke_gen_chain = RunnableSequence(prompt, model, parser)

parallel_chain = RunnableParallel({'joke': RunnablePassthrough(),
                                   'word_count': RunnableLambda(word_count)
                                   })

final_chain = RunnableSequence(joke_gen_chain, parallel_chain)
result = final_chain.invoke({'topic':'AI'})
final_result = """{} \nTotal word count - {}""".format(result['joke'], result['word_count'])
print(final_result)
from langchain_huggingface import ChatHuggingFace,HuggingFacePipeline
llm = HuggingFacePipeline.from_model_id(
    model_id='TinyLlama/TinyLlama-1.1B-chat-v1.0',
    task="text-generation",
    pipeline_kwargs=dict(temperature=0.5, max_new_tokens=100)
)
model=HuggingFacePipeline(llm=llm)

response = model.invoke("What is the capital of India?")
print(response)
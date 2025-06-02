from langchain.text_splitter import RecursiveCharacterTextSplitter

text = """LangChain is a powerful framework designed to simplify the development of applications that use large language models (LLMs). Its core components include PromptTemplates, which standardize how inputs are passed to models, and LLMs, which provide interfaces to models like GPT. Chains allow combining multiple components (like prompts, tools, and models) to form complex workflows. Agents enable dynamic decision-making by choosing which tools or chains to invoke based on user input. Document Loaders, Text Splitters, Retrievers, and Vector Stores support working with external data, enabling retrieval-augmented generation (RAG). Together, these components make it easier to build robust, modular, and intelligent LLM-powered applications."""

splitter = RecursiveCharacterTextSplitter(chunk_size = 150,
                                          chunk_overlap = 20)

chunks = splitter.split_text(text)
print(len(chunks))
print(chunks[0])
print(chunks[1])
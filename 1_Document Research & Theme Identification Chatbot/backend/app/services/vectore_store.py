# Embedding + Vector DB with Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import CharacterTextSplitter
import os

CHROMA_PATH = "backend/data/chroma_db"

embedding_model = OpenAIEmbeddings()
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)

def store_text(text, doc_id):
    chunks = text_splitter.split_text(text)
    metadatas = [{"source": doc_id}] * len(chunks)
    
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)
    db.add_texts(chunks, metadatas=metadatas)
    db.persist()

def query_text(query):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_model)
    return db.similarity_search_with_score(query, k=5)

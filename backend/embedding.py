from langchain_community.vectorstores.faiss import FAISS
from langchain_community.embeddings.openai import OpenAIEmbeddings

def embed_files(files, openai_api_key=None):
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return FAISS.from_documents(files, embeddings)

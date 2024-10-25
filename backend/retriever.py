# retriever.py
import streamlit as st
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

class FaissRetriever:
    def __init__(self, documents):
        # Retrieve the OpenAI API Key from Streamlit secrets
        api_key = st.secrets["OPENAI_API_KEY"]
        
        # Initialize embeddings with the API key
        embeddings = OpenAIEmbeddings(openai_api_key=api_key)
        
        # Initialize the FAISS index with the documents and embeddings
        self.index = FAISS.from_documents(documents, embeddings)
        print("FAISS index initialized with documents metadata.")

    def retrieve(self, query):
        # Perform similarity search in the FAISS index
        results = self.index.similarity_search(query, k=5)
        for result in results:
            print(f"Retrieved match metadata: {result.metadata}")  # Check if pdf_path is retained
        return results

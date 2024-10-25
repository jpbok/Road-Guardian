# retriever.py
import streamlit as st
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
print("st.secrets:", st.secrets)

class FaissRetriever:
    def __init__(self, documents):
        # Check if API key is in st.secrets and print debug information
        if "OPENAI_API_KEY" in st.secrets:
            print("API key found!")
            api_key = st.secrets["OPENAI_API_KEY"]
        else:
            print("API key not found! Please set it in Streamlit secrets.")
            raise KeyError("OPENAI_API_KEY is missing in Streamlit secrets.")

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

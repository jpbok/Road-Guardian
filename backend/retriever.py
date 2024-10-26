# retriever.py
import streamlit as st
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings

class FaissRetriever:
    def __init__(self, documents):
        # Replace OpenAI base URL and model to use GovText settings
        api_key = st.secrets["GOVTEXT_API_KEY"]
        embeddings = OpenAIEmbeddings(
            openai_api_key=api_key,
            openai_api_base="https://litellm.govtext.gov.sg/",
            model="text-embedding-3-large-prd-gcc2-lb"
        )
        self.index = FAISS.from_documents(documents, embeddings)

    def retrieve(self, query):
        return self.index.similarity_search(query, k=5)

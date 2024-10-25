# retriever.py
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document

class FaissRetriever:
    def __init__(self, documents):
        # Ensure the OpenAIEmbeddings includes pdf_path metadata in the index
        embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API_KEY"])
        self.index = FAISS.from_documents(documents, embeddings)
        print("FAISS index initialized with documents metadata.")

    def retrieve(self, query):
        results = self.index.similarity_search(query, k=5)
        for result in results:
            print(f"Retrieved match metadata: {result.metadata}")  # Check if pdf_path is retained
        return results

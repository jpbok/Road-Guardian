# retriever.py
from backend.govtext_api import get_response_from_llm
from langchain.vectorstores.faiss import FAISS
from langchain.docstore.document import Document

class FaissRetriever:
    def __init__(self, documents):
        # Here, we directly get embeddings from GovText, if supported
        embeddings = [get_response_from_llm(doc.page_content) for doc in documents]
        self.index = FAISS.from_texts([doc.page_content for doc in documents], embeddings)
        print("FAISS index initialized with documents metadata.")

    def retrieve(self, query):
        results = self.index.similarity_search(query, k=5)
        for result in results:
            print(f"Retrieved match metadata: {result.metadata}")
        return results

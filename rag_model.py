from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize

class RAGModel:
    def __init__(self):
        # Initialize sentence-transformer model and FAISS index.
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')
        self.index = None
        self.documents = []

    def chunk_text(self, text):
        """Split text into sentences (or paragraphs) for easier retrieval."""
        return sent_tokenize(text)

    def build_index(self, document_list):
        """Create embeddings and FAISS index from a list of documents."""
        self.documents = document_list
        embeddings = self.model.encode(document_list)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings))

    def retrieve_documents(self, query, top_k=3):
        """Retrieve the most relevant documents based on the query."""
        if not self.index:
            raise ValueError("The index has not been built.")
        query_embedding = self.model.encode([query])
        distances, indices = self.index.search(query_embedding, top_k)
        return [self.documents[idx] for idx in indices[0]]

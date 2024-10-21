from langchain.chains import RetrievalQA
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import OpenAI
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from backend.retriever import DocumentRetriever
from backend.optimization import (
    recursive_splitter,
    semantic_chunker,
    query_transform,
    query_router,
    context_compressor,
    prompt_compressor
)

class RAGModel:
    def __init__(self, openai_api_key):
        self.openai_api_key = openai_api_key
        self.llm = OpenAI(temperature=0, api_key=openai_api_key)
        self.retriever, self.doc_retriever = self.initialize_retriever()

    def initialize_retriever(self):
        """Initializes the document retriever and vector store."""
        doc_retriever = DocumentRetriever()
        all_docs = [doc for doc in doc_retriever.docs.values()]
        all_docs = recursive_splitter(all_docs)
        all_docs = semantic_chunker(all_docs)
        embeddings = OpenAIEmbeddings(api_key=self.openai_api_key)
        vector_store = FAISS.from_texts(all_docs, embeddings)
        compressor = LLMChainExtractor.from_llm(self.llm)
        compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=vector_store.as_retriever()
        )
        return compression_retriever, doc_retriever

    def chunk_text(self, text, max_length=2000):
        """Chunks text into smaller pieces."""
        return [text[i:i + max_length] for i in range(0, len(text), max_length)]

    def answer_question(self, query):
        """Answers the user's query using the RAG model."""
        transformed_query = query_transform(query)
        routed_query = query_router(transformed_query)
        
        retrieval_qa = RetrievalQA.from_chain_type(
            retriever=self.retriever,
            llm=self.llm,
            chain_type="map_reduce"
        )
        
        context = retrieval_qa.run(routed_query)
        context = context_compressor(context, self.llm, self.retriever)

        context_chunks = self.chunk_text(context, max_length=4097 - 256)
        responses = []
        for chunk in context_chunks:
            compressed_prompt = prompt_compressor(chunk)
            messages = [
                {"role": "system", "content": "You are a chatbot that assists learner drivers by summarizing driving theory, providing test preparation tips, and explaining test results."},
                {"role": "user", "content": query},
                {"role": "assistant", "content": compressed_prompt}
            ]
            response = self.llm.chat_completions.create(model="gpt-3.5-turbo", messages=messages)
            responses.append(response['choices'][0]['message']['content'])
        
        return ' '.join(responses)

# Example usage:
# rag_model = RAGModel(openai_api_key="your-openai-api-key")
# answer = rag_model.answer
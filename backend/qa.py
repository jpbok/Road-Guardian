from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from backend.embedding import FolderIndex
from langchain.chat_models import ChatOpenAI

class AnswerWithSources:
    def __init__(self, answer, sources):
        self.answer = answer
        self.sources = sources

def query_folder(query: str, folder_index: FolderIndex) -> AnswerWithSources:
    llm = ChatOpenAI(model="gpt-3.5-turbo")
    chain = load_qa_with_sources_chain(llm)
    relevant_docs = folder_index.index.similarity_search(query, k=5)
    result = chain({"input_documents": relevant_docs, "question": query})
    answer = result["output_text"].split("SOURCES: ")[0]
    sources = relevant_docs
    return AnswerWithSources(answer=answer, sources=sources)

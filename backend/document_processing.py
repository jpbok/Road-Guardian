import json
from langchain.docstore.document import Document
from backend.retriever import FaissRetriever
from backend.govtext_api import get_response_from_llm

def load_documents_from_metadata(metadata_paths):
    documents = []
    for path in metadata_paths:
        with open(path, 'r') as f:
            metadata_entries = json.load(f)
            for entry in metadata_entries:
                document = Document(
                    page_content=entry["content"],
                    metadata={
                        "page": entry["metadata"].get("page"),
                        "chunk": entry["metadata"].get("chunk"),
                        "pdf_path": entry["metadata"].get("pdf_path", path)
                    }
                )
                documents.append(document)
    return documents

def generate_mcqs_from_response(response_text):
    prompt = (
        f"Based on the following driving theory text, create three multiple-choice questions with 3 answer options each. "
        f"Each question should have only one correct answer. Provide the correct answer after each question.\n\n"
        f"Text:\n{response_text}\n\nMCQs:\n"
    )
    return get_response_from_llm(prompt)

def handle_query_submission(query, metadata_paths, image_folder=None):
    documents = load_documents_from_metadata(metadata_paths)
    faiss_retriever = FaissRetriever(documents)
    matches = faiss_retriever.retrieve(query)
    query_text = "\n".join([match.page_content for match in matches])
    llm_response = get_response_from_llm(query_text)
    mcqs = generate_mcqs_from_response(llm_response)
    return matches, llm_response, mcqs

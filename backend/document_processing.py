import json
import streamlit as st
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
                        "pdf_path": entry["metadata"].get("pdf_path", path),
                        "images": entry["metadata"].get("images", [])
                    }
                )
                documents.append(document)
    return documents

def format_mcqs(mcq_response):
    """Formats the MCQs to have each question and corresponding answer clearly separated."""
    formatted_mcqs = ""
    questions = mcq_response.split("\n")
    question_number = 1

    for line in questions:
        if line.startswith("Question") or line.startswith("What") or line.endswith("?"):
            formatted_mcqs += f"**{line.strip()}**\n\n"  # Bold the question
        elif line.startswith("Correct Answer"):
            formatted_mcqs += f"{line.strip()}\n\n---\n\n"  # Add line separators after answers
        else:
            formatted_mcqs += f"{line.strip()}\n"  # Normal answer choices

    return formatted_mcqs


def generate_mcqs_from_response(response_text):
    prompt = (
        f"Based on the following driving theory text, create three multiple-choice questions with 3 answer options each. "
        f"Each question should have only one correct answer. Provide the correct answer after each question.\n\n"
        f"Text:\n{response_text}\n\nMCQs:\n"
    )
    mcq_response = get_response_from_llm(prompt)
    return format_mcqs(mcq_response)

def handle_query_submission(query, metadata_paths, image_folder=None):
    documents = load_documents_from_metadata(metadata_paths)
    faiss_retriever = FaissRetriever(documents)
    matches = faiss_retriever.retrieve(query)
    query_text = "\n".join([match.page_content for match in matches])
    llm_response = get_response_from_llm(query_text)
    mcqs = generate_mcqs_from_response(llm_response)

    # Append a note to encourage users to refer to the theory book details and images
    if matches:
        additional_note = "\n\nFor more detailed information, please refer to the matched pages above and accompanying images from the theory books."
        llm_response += additional_note

    return matches, llm_response, mcqs

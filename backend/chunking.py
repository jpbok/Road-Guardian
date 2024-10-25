# chunking.py
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_file(file, chunk_size, chunk_overlap, pdf_path):
    """Chunks each document, ensuring pdf_path is added to each chunk's metadata."""
    chunked_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for i, chunk in enumerate(text_splitter.split_documents([file])):
        chunk.metadata.update({
            "pdf_path": pdf_path,
            "chunk_number": i + 1  # For tracking purposes
        })
        chunked_docs.append(chunk)
        print(f"Chunk metadata with pdf_path: {chunk.metadata}")  # Debugging line to verify pdf_path

    return chunked_docs

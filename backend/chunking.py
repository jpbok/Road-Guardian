from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_file(file, chunk_size, chunk_overlap, pdf_path, image_metadata=None):
    """Chunks each document, ensuring pdf_path and image metadata are added to each chunk's metadata."""
    chunked_docs = []
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

    for doc in file.docs:  # Iterate over Document objects in the File
        for i, chunk in enumerate(text_splitter.split_documents([doc])):
            chunk.metadata.update({
                "pdf_path": pdf_path,
                "chunk_number": i + 1  # For tracking purposes
            })
            if image_metadata:
                page_number = chunk.metadata.get("page")
                chunk.metadata["images"] = [
                    image["image_path"] for image in image_metadata if image["page"] == page_number
                ]
            chunked_docs.append(chunk)
            print(f"Chunk metadata with pdf_path and images: {chunk.metadata}")  # Debugging line

    return chunked_docs

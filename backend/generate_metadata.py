import os
import json
from backend.parsing import read_file
from backend.chunking import chunk_file
from backend.embedding import embed_files

def generate_metadata(pdf_paths, output_metadata_file, chunk_size=300):
    files = [chunk_file(read_file(path), chunk_size=chunk_size) for path in pdf_paths]
    folder_index = embed_files(files)
    metadata = []
    for file in files:
        for doc in file.docs:
            metadata.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "embedding": None,  # Placeholder if embeddings are needed
            })
    with open(output_metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

# Generate metadata for driver and rider documents
generate_metadata(["documents/basic_theory.pdf", "documents/final_theory.pdf"], "documents/chunks/driver_metadata.json")
generate_metadata(["documents/basic_theory.pdf", "documents/riding_theory.pdf"], "documents/chunks/rider_metadata.json")

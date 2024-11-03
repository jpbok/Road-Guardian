import os
import json
from backend.parsing import read_file
from backend.chunking import chunk_file
from backend.embedding import embed_files

# Load image metadata from image_metadata.json
with open("assets/images/image_metadata.json", "r") as img_meta_file:
    image_metadata = json.load(img_meta_file)

def generate_metadata(pdf_paths, output_metadata_file, chunk_size=300):
    files = [read_file(path) for path in pdf_paths]
    metadata = []

    for file in files:
        pdf_name = os.path.basename(file.name)  # Ensure we use the base name
        chunked_docs = chunk_file(file, chunk_size=chunk_size, chunk_overlap=50, pdf_path=file.name)

        for doc in chunked_docs:
            page = doc.metadata.get("page")
            images_for_page = [
                img["image_path"] for img in image_metadata.get(f"./documents/{pdf_name}", [])
                if img["page"] == page
            ]
            
            doc.metadata["images"] = images_for_page  # Add images to the metadata
            metadata.append({
                "content": doc.page_content,
                "metadata": doc.metadata,
                "embedding": None,  # Placeholder for embeddings
            })

    with open(output_metadata_file, 'w') as f:
        json.dump(metadata, f, indent=4)

# Generate metadata for driver and rider documents
generate_metadata(["documents/basic_theory.pdf", "documents/final_theory.pdf"], "documents/chunks/driver_metadata.json")
generate_metadata(["documents/basic_theory.pdf", "documents/riding_theory.pdf"], "documents/chunks/rider_metadata.json")

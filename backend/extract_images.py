import os
from pdf2image import convert_from_path
import json

def extract_images_from_pdf(pdf_path, output_folder):
    """Extracts images from each page of a PDF and saves them to the specified folder with a consistent naming pattern."""
    try:
        if not os.path.exists(pdf_path):
            print(f"PDF file not found: {pdf_path}")
            return []

        images = convert_from_path(pdf_path)
        saved_image_paths = []

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # Naming convention: image_<pdf_name>_page_<page_number>.png
        pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
        for i, image in enumerate(images):
            page_number = i + 1
            image_filename = f"image_{pdf_name}_page_{page_number}.png"
            image_path = os.path.join(output_folder, image_filename)
            image.save(image_path, 'PNG')
            saved_image_paths.append({"page": page_number, "image_path": image_path})

        print(f"Images successfully extracted to {output_folder}")
        return saved_image_paths

    except Exception as e:
        print(f"Error extracting images: {e}")
        return []

if __name__ == "__main__":
    pdfs_and_folders = [
        ("documents/basic_theory.pdf", "assets/images/basic_theory"),
        ("documents/final_theory.pdf", "assets/images/final_theory"),
        ("documents/riding_theory.pdf", "assets/images/riding_theory"),
    ]

    all_images_metadata = {}
    for pdf_path, output_folder in pdfs_and_folders:
        extracted_images = extract_images_from_pdf(pdf_path, output_folder)
        all_images_metadata[pdf_path] = extracted_images

    # Save metadata to JSON
    with open("assets/images/image_metadata.json", "w") as f:
        json.dump(all_images_metadata, f, indent=4)

    print("Image metadata saved to assets/images/image_metadata.json")

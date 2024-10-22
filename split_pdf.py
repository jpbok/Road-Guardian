import os
import PyPDF2

def split_pdf(file_path, output_dir):
    """Splits PDF into chunks and saves them as separate files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(file_path, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        total_pages = len(reader.pages)
        
        for i in range(total_pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            chunk_path = os.path.join(output_dir, f'basic_theory_chunk_{i+1}.pdf')
            with open(chunk_path, 'wb') as outfile:
                writer.write(outfile)

# Usage
split_pdf('documents/basic_theory.pdf', 'documents/chunks')

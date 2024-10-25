import os
import PyPDF2

def split_pdf(file_path, output_dir, prefix):
    """Splits PDF into chunks and saves them as separate files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    with open(file_path, 'rb') as infile:
        reader = PyPDF2.PdfReader(infile)
        total_pages = len(reader.pages)
        
        for i in range(total_pages):
            writer = PyPDF2.PdfWriter()
            writer.add_page(reader.pages[i])
            chunk_path = os.path.join(output_dir, f'{prefix}_chunk_{i+1}.pdf')
            with open(chunk_path, 'wb') as outfile:
                writer.write(outfile)

# Usage
split_pdf('documents/basic_theory.pdf', 'documents/chunks', 'basic_theory')
split_pdf('documents/final_theory.pdf', 'documents/chunks', 'final_theory')
split_pdf('documents/riding_theory.pdf', 'documents/chunks', 'riding_theory')

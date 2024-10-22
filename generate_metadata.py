import json
import os
import PyPDF2
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
import nltk

# Ensure NLTK components are downloaded
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

def extract_keywords(text, num_keywords=5):
    """Extracts keywords from the text."""
    words = word_tokenize(text)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]
    fdist = FreqDist(filtered_words)
    keywords = [word for word, frequency in fdist.most_common(num_keywords)]
    return keywords

metadata = []

def generate_metadata(output_dir):
    """Generates metadata for each PDF chunk."""
    for chunk_file in os.listdir(output_dir):
        if chunk_file.endswith('.pdf'):
            chunk_path = os.path.join(output_dir, chunk_file)
            text = extract_text_from_pdf(chunk_path)
            summary = ' '.join(text.split()[:50])  # Simple summary: first 50 words
            keywords = extract_keywords(text)
            metadata.append({
                "path": chunk_path,
                "summary": summary,
                "keywords": keywords,
                "page_number": chunk_file.split('_')[-1].split('.')[0]
            })
    
    with open(os.path.join(output_dir, 'metadata.json'), 'w') as f:
        json.dump(metadata, f, indent=4)

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Usage
generate_metadata('documents/chunks')

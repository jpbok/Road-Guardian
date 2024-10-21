import os
import PyPDF2
import pandas as pd
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Path to the documents folder
DOCUMENTS_DIR = os.path.join(os.getcwd(), 'documents')

class DocumentRetriever:
    def __init__(self):
        self.docs = self.load_documents()

    def load_documents(self):
        """Load PDF documents from the documents folder."""
        documents = {}
        for file_name in os.listdir(DOCUMENTS_DIR):
            if file_name.endswith('.pdf'):
                file_path = os.path.join(DOCUMENTS_DIR, file_name)
                documents[file_name] = self.extract_text_from_pdf(file_path)
        return documents

    def extract_text_from_pdf(self, file_path):
        """Extracts text from a PDF file."""
        with open(file_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        return text

    def recursive_split(self, text):
        """Perform recursive splitting of text."""
        splitter = RecursiveCharacterTextSplitter()
        return splitter.split(text)

    def search_documents(self, query):
        """Search through the loaded documents and return the most relevant passages."""
        results = []
        for doc_name, text in self.docs.items():
            if query.lower() in text.lower():
                results.append({'document': doc_name, 'text': text})
        return results

    def load_checklist_data(self):
        """Load checklist data from a CSV."""
        csv_path = os.path.join(os.getcwd(), 'data', 'driving_checklists.csv')
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        return None

# Example usage:
# retriever = DocumentRetriever()
# result = retriever.search_documents("traffic rules")
# print(result)

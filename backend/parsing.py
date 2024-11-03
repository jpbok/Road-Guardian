import fitz  # PyMuPDF
import os  # Import the os module
from langchain.docstore.document import Document
from io import BytesIO
from hashlib import md5

class File:
    def __init__(self, name: str, id: str, docs=None):
        self.name = name
        self.id = id
        self.docs = docs or []

    def copy(self):
        return File(self.name, self.id, [doc for doc in self.docs])

class PdfFile(File):
    @classmethod
    def from_bytes(cls, file: BytesIO, name: str) -> "PdfFile":
        pdf = fitz.open(stream=file.read(), filetype="pdf")
        docs = [Document(page_content=page.get_text("text"), metadata={"page": i + 1}) for i, page in enumerate(pdf)]
        return cls(name=name, id=md5(file.read()).hexdigest(), docs=docs)

def read_file(file_path: str) -> PdfFile:
    with open(file_path, "rb") as f:
        return PdfFile.from_bytes(BytesIO(f.read()), name=os.path.basename(file_path))

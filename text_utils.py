import os
from io import BytesIO
from PyPDF2 import PdfReader
import docx2txt
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_and_split_text(uploaded_file, chunk_size=1000, chunk_overlap=100):
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    if ext == ".pdf":
        text = _read_pdf(uploaded_file)
    elif ext == ".docx":
        text = _read_docx(uploaded_file)
    elif ext == ".txt":
        text = _read_txt(uploaded_file)
    else:
        raise ValueError(f"Unsupported file type: {ext}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_text(text)
    return chunks

def _read_pdf(file):
    pdf_reader = PdfReader(BytesIO(file.read()))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

def _read_docx(file):
    return docx2txt.process(BytesIO(file.read()))

def _read_txt(file):
    return file.read().decode("utf-8")

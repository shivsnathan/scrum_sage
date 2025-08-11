import streamlit as st
import pdfplumber
import docx
import pandas as pd

def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    paragraphs = [p.text for p in doc.paragraphs]
    return "\n".join(paragraphs)

def extract_text_from_csv_or_xlsx(file):
    try:
        df = pd.read_csv(file)
    except Exception:
        df = pd.read_excel(file)
    return df.to_csv(index=False)

def extract_text_from_txt(file):
    return file.read().decode("utf-8", errors="ignore")

def upload_and_extract_text():
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "csv", "xlsx", "txt"])

    if uploaded_file is not None:
        file_type = uploaded_file.type
        st.write(f"Uploaded file type: {file_type}")
        text = ""

        if file_type == "application/pdf":
            text = extract_text_from_pdf(uploaded_file)
        elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            text = extract_text_from_docx(uploaded_file)
        elif file_type in ["text/csv", "application/vnd.ms-excel"]:
            text = extract_text_from_csv_or_xlsx(uploaded_file)
        elif file_type == "text/plain":
            text = extract_text_from_txt(uploaded_file)
        else:
            st.error("Unsupported file type")
            return None, None

        if text:
            st.text_area("Extracted Text", text, height=300)
            return uploaded_file, text
        else:
            st.warning("No text could be extracted from this file.")
            return None, None
    else:
        return None, None

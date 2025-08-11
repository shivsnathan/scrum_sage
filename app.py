import streamlit as st
from text_utils import load_and_split_text
from vector_store import VectorStore

vector_store = VectorStore()
vector_store.load()

def handle_file_upload():
    uploaded_files = st.file_uploader("Upload Sprint Docs", type=["pdf", "docx", "txt"], accept_multiple_files=True)
    if uploaded_files:
        for file in uploaded_files:
            st.write(f"Processing: {file.name}")
            chunks = load_and_split_text(file)
            vector_store.add_texts(chunks)
        st.success("All files processed and indexed.")

def handle_query():
    query = st.text_input("Ask a question about your sprint, user stories, or requirements:")
    if query:
        results = vector_store.similarity_search(query, k=3)
        if results:
            st.subheader("Top Matches")
            for i, doc in enumerate(results, 1):
                st.write(f"**Match {i}:** {doc.page_content}")
        else:
            st.warning("No relevant information found.")

def main():
    st.set_page_config(page_title="Scrum Sage", layout="wide")
    st.title("📊 Scrum Sage - Sprint Insights Chatbot")

    page = st.sidebar.radio("Choose action", ["Upload Docs", "Ask Questions"])

    if page == "Upload Docs":
        handle_file_upload()
    else:
        handle_query()

if __name__ == "__main__":
    main()

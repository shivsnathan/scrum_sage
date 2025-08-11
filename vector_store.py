from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DB_FAISS_PATH = "faiss_index"

class VectorStore:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        self.vector_store = None

    def add_texts(self, texts):
        # Create or update FAISS vector store with text chunks
        if self.vector_store:
            # Add to existing index (you can implement incremental add here)
            # For simplicity, recreate index every time:
            all_texts = [d.page_content for d in self.vector_store.docstore._dict.values()] + texts
            self.vector_store = FAISS.from_texts(all_texts, self.embeddings)
        else:
            self.vector_store = FAISS.from_texts(texts, self.embeddings)

        self.vector_store.save_local(DB_FAISS_PATH)

    def load(self):
        try:
            self.vector_store = FAISS.load_local(DB_FAISS_PATH, self.embeddings, allow_dangerous_deserialization=True)
        except Exception:
            self.vector_store = None

    def similarity_search(self, query, k=3):
        if not self.vector_store:
            self.load()
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=k)

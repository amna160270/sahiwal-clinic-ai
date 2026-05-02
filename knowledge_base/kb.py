from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


class MedicalKnowledgeBase:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.db = None

    def build_db(self, file_path="data/medical.txt"):
        loader = TextLoader(file_path, encoding="utf-8")
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )

        chunks = splitter.split_documents(docs)
        self.db = FAISS.from_documents(chunks, self.embeddings)

    def search(self, query):
        if not self.db:
            return "No knowledge base loaded"

        docs = self.db.similarity_search(query, k=3)
        return "\n".join([d.page_content for d in docs])
from langchain_community.document_loaders import TextLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings


class RAGTool:
    def __init__(self, knowledge_base_path="knowledge_base"):
        self.path = knowledge_base_path
        self.vectorstore = None
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

    def load_and_index(self):
        print("📚 Documents load ho rahe hain...")
        loader = DirectoryLoader(
            self.path,
            glob="*.txt",
            loader_cls=TextLoader,
            loader_kwargs={"encoding": "utf-8"}
        )
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        chunks = splitter.split_documents(documents)
        self.vectorstore = FAISS.from_documents(chunks, self.embeddings)
        print(f"✅ {len(documents)} documents, {len(chunks)} chunks indexed!")

    def retrieve(self, query, k=3):
        if not self.vectorstore:
            return "No documents loaded."
        results = self.vectorstore.similarity_search(query, k=k)
        return "\n\n".join([r.page_content for r in results])

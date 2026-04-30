import os
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

class SyllabusVectorStore:
    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "syllabus"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        
        # API 키 확인
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("[!] 경고: GOOGLE_API_KEY가 설정되지 않았습니다.")

        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory
        )

    def add_documents(self, documents):
        """LangChain Document 객체들을 벡터 스토어에 추가합니다."""
        return self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4):
        """유사한 강의를 검색합니다."""
        return self.vector_store.similarity_search(query, k=k)

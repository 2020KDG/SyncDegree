import os
import json
import asyncio
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from database.vector_store import SyllabusVectorStore
from dotenv import load_dotenv

load_dotenv()

async def ingest_data():
    """
    Crawled JSON 데이터를 읽어와 LangChain Document 객체로 변환하고
    ChromaDB 벡터 스토어에 적재하는 스크립트.
    """
    print("--- 데이터 적재 시작 ---")

    # 벡터 스토어 초기화
    vector_store_manager = SyllabusVectorStore()
    
    # 데이터 폴더 경로
    data_dir = "data"
    
    if not os.path.exists(data_dir):
        print(f"경고: 데이터 폴더 ({data_dir})를 찾을 수 없습니다. 크롤링을 먼저 실행해주세요.")
        return

    json_files = [f for f in os.listdir(data_dir) if f.endswith('.json')]

    if not json_files:
        print(f"경고: {data_dir} 폴더에 JSON 파일이 없습니다. 크롤링을 먼저 실행해주세요.")
        return

    all_documents = []

    for json_file in json_files:
        file_path = os.path.join(data_dir, json_file)
        university_name = os.path.splitext(json_file)[0] # 파일 이름에서 대학 이름 추출 (예: 원광대학교.json -> 원광대학교)
        print(f"[*] {university_name} 데이터 읽는 중: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            lectures_data = json.load(f)
        
        for lecture in lectures_data:
            # LangChain Document 객체 생성
            # page_content: 임베딩 및 검색에 사용될 주요 텍스트
            # metadata: 강의의 추가 정보
            page_content = (
                f"대학교: {lecture.get('university', '')}
"
                f"학과: {lecture.get('department', '')}
"
                f"과목명: {lecture.get('course_title', '')}
"
                f"교수: {lecture.get('professor', '')}
"
                f"학습 목표: {lecture.get('learning_objective', '')}
"
                # 추가적인 상세 내용이 있다면 여기에 포함
            )
            
            metadata = {
                "university": lecture.get("university", ""),
                "department": lecture.get("department", ""),
                "course_title": lecture.get("course_title", ""),
                "professor": lecture.get("professor", ""),
                "learning_objective": lecture.get("learning_objective", ""),
                "syllabus_url": lecture.get("syllabus_url", "")
            }
            
            all_documents.append(Document(page_content=page_content, metadata=metadata))
    
    if all_documents:
        print(f"[!] 총 {len(all_documents)}개의 강의 문서를 벡터 스토어에 추가합니다.")
        vector_store_manager.add_documents(all_documents)
        print("--- 데이터 적재 완료 ---")
    else:
        print("적재할 문서가 없습니다.")

if __name__ == "__main__":
    asyncio.run(ingest_data())

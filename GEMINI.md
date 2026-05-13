# Edu-LocalUp Project Mandates

이 파일은 "에듀-로컬업" 프로젝트의 모든 컴퓨터(Gemini CLI)에서 동일한 작업 원칙을 유지하기 위한 공유 지침입니다.

## 1. 프로젝트 아키텍처 원칙
- **지능형 RAG 우선**: 단순 벡터 검색이 아닌, LLM이 쿼리 확장 및 최종 강의 선별을 담당하는 로직을 준수할 것.
- **데이터 출처**: 대학 강의계획서 크롤링 데이터를 최우선으로 하며, 부족한 경우 LLM 보정을 사용할 것.
- **기술 스택**: FastAPI, LangChain, Gemini API, ChromaDB, Tailwind CSS 사용.

## 2. 개발 워크플로우
- 모든 API 기능은 테스트 코드를 포함해야 함.
- UI는 Tailwind CSS를 활용하여 현대적이고 깔끔한 디자인을 유지할 것.
- 환경 변수는 `.env` 파일에서 관리하며, 비밀 키가 커밋되지 않도록 주의할 것.

## 3. 커리큘럼 생성 규칙
- 결과물은 항상 '입문 - 중급 - 심화'의 3단계 구조를 가져야 함.
- 각 단계별로 왜 이 강의가 선택되었는지에 대한 '추천 사유'를 포함해야 함.

## 4. 팀원 로컬 환경 설정 (Python & MCP)
이 프로젝트는 **Python 3.10 이상** 환경이 필요합니다.

```powershell
# 1. Python 설치 (3.10+ 권장)
# https://www.python.org/downloads/ 에서 설치 시 "Add Python to PATH" 체크 필수

# 2. 가상환경 생성 및 패키지 설치
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# 3. 브라우저 엔진 설치 (Playwright)
npx playwright install
```

## 5. 프로젝트 디렉토리 구조
- `crawlers/`: 대학별 강의계획서 수집 로직
- `database/`: ChromaDB 연동 및 데이터 관리 (`vector_store.py`)
- `data/`: 수집된 JSON 데이터 저장소
- `tests/`: 단위 및 통합 테스트 코드

## 6. 현재 진행 상황 (2026-04-30 기준)
- [x] 프로젝트 기획서(`project_plan.md`) 작성 완료
- [x] 기본 폴더 구조 및 `requirements.txt` 생성 완료
- [x] 건양대 프로토타입 크롤러 작성 완료
- [x] ChromaDB 기반 벡터 스토어 매니저(`database/vector_store.py`) 구현 완료
- [x] **원광대 강의계획서 크롤러(`crawlers/wonkwang.py`) 구현 및 테스트 완료**

### 다음 작업 단계
1. [x] **수집된 JSON 데이터를 벡터 DB에 일괄 적재하는 스크립트 작성.**
2. 건양대 크롤러의 팝업 처리 로직 고도화 (원광대 방식 참고).
3. FastAPI 기반의 강의 추천 API 엔드포인트 개발.

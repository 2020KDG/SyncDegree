# Edu-LocalUp Project Memory

이 파일은 프로젝트의 비정형적인 기억과 컨텍스트를 저장합니다. 다른 환경에서 작업을 재개할 때 Gemini가 이 파일을 읽어 이전의 판단 근거를 파악할 수 있습니다.

## 크롤링 전략 (원광대학교)
- **URL 구조**: `lectRPlanView.jsp` 팝업은 `codeLesson`, `classNo`, `employeeNo` 세 가지 핵심 파라미터가 필요함.
- **브라우저 관리**: Playwright 사용 시 `Page` 객체를 재사용하여 속도를 최적화함. (Task 1 & 2 개선 사항)
- **데이터 정제**: 원광대 웹사이트의 인코딩 문제로 인해 수집 시 한글 깨짐 현상이 발생할 수 있으나, Playwright의 `innerText`를 통해 텍스트로 가져오면 브라우저가 자동으로 디코딩함.

## 벡터 DB (ChromaDB)
- `database/vector_store.py`에 기본 매니저가 구현되어 있음.
- `tests/test_vector_store.py`를 통해 임베딩 및 검색 기능 검증됨.

## 환경 변수
- `.env` 파일에 `GOOGLE_API_KEY` 설정이 필요함. (보안상 공유 금지)

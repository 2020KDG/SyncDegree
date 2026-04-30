import asyncio
from playwright.async_api import async_playwright
from crawlers.base import BaseCrawler
from bs4 import BeautifulSoup

class KonyangCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(
            university_name="건양대학교",
            base_url="https://www.konyang.ac.kr/prog/sueopgyehoek/kor/sub06_01_04_02/list.do"
        )

    async def run(self):
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            # 건양대 강의계획서 페이지 접속
            await page.goto(self.base_url)
            
            # 학과 리스트 가져오기 (예시로 첫 번째 학과만 크롤링)
            # 실제 구현 시에는 모든 학과를 순회하도록 개발 예정
            content = await page.content()
            soup = BeautifulSoup(content, "html.parser")
            
            # 강의 목록 테이블 파싱
            rows = soup.select("#txt > div.b-table01.type02 > table > tbody > tr")
            
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 8: continue
                
                title = cols[1].text.strip()
                professor = cols[5].text.strip()
                # 학과 정보가 보통 3번째 컬럼(index 3)에 위치함
                dept = cols[3].text.strip() if len(cols) > 3 else "공통"
                
                # 상세 페이지(수업계획서) 링크 추출
                # 실제 구현 시 page.expect_popup()을 사용하여 팝업 내용을 읽어야 함
                objective = "상세 강의 목표 수집 예정 (팝업 처리 필요)"
                detail_link = self.base_url 
                
                self.add_lecture(
                    title=title,
                    professor=professor,
                    department=dept,
                    objective=objective,
                    url=detail_link
                )
            
            await browser.close()
            self.save_results()

if __name__ == "__main__":
    crawler = KonyangCrawler()
    asyncio.run(crawler.run())

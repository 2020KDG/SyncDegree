import asyncio
import json
from crawlers.wonkwang import WonkwangCrawler

async def verify_syllabus():
    crawler = WonkwangCrawler()
    async with crawler:
        # User provided example URL (slightly modified for potential validity)
        url = "https://intra.wku.ac.kr/SWupis/V005/Service/Teach/HLecPlan/lectRPlanView.jsp?codeCollege=XX&year=2026&term=1&codeLesson=L00002&classNo=44&employeeNo=92097"
        print(f"Scraping syllabus from: {url}")
        details = await crawler.scrape_syllabus(url)
        print("\n[Scraped Details]")
        print(json.dumps(details, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(verify_syllabus())

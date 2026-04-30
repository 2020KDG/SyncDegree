import asyncio
from crawlers.wonkwang import WonkwangCrawler

async def dump_syllabus():
    async with WonkwangCrawler() as crawler:
        colleges = await crawler.get_colleges()
        if colleges:
            dept = await crawler.get_departments(colleges[0]['value'])
            if dept:
                courses = await crawler.scrape_timetable(colleges[0]['value'], dept[0]['value'])
                if courses:
                    url = courses[0]['syllabus_url']
                    print(f"Dumping syllabus from: {url}")
                    await crawler.page.goto(url)
                    await crawler.page.wait_for_load_state("networkidle")
                    content = await crawler.page.content()
                    with open("syllabus_sample.html", "w", encoding="utf-8") as f:
                        f.write(content)
                    print("Dumped to syllabus_sample.html")

if __name__ == "__main__":
    asyncio.run(dump_syllabus())

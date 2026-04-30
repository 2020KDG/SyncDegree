import asyncio
from crawlers.wonkwang import WonkwangCrawler

async def reproduce():
    try:
        async with WonkwangCrawler() as crawler:
            print("Crawler started successfully")
            colleges = await crawler.get_colleges()
            if colleges:
                print(f"Found {len(colleges)} colleges")
                dept = await crawler.get_departments(colleges[0]['value'])
                if dept:
                    print(f"Found {len(dept)} departments")
                    courses = await crawler.scrape_timetable(colleges[0]['value'], dept[0]['value'])
                    print(f"Found {len(courses)} courses")
    except SyntaxError as e:
        print(f"Caught SyntaxError: {e}")
    except AttributeError as e:
        print(f"Caught AttributeError: {e}")
    except Exception as e:
        print(f"Caught Exception: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(reproduce())

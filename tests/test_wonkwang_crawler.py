import pytest
import asyncio
from crawlers.wonkwang import WonkwangCrawler

@pytest.mark.asyncio
async def test_wonkwang_crawler_lifecycle():
    crawler = WonkwangCrawler()
    # Explicit start/stop
    await crawler.start()
    try:
        colleges = await crawler.get_colleges()
        assert isinstance(colleges, list)
        assert len(colleges) > 0
        
        kyohak = next((c for c in colleges if '교학' in c['label']), None)
        assert kyohak is not None
        
        depts = await crawler.get_departments(kyohak['value'])
        assert isinstance(depts, list)
        assert len(depts) > 0
        
        won = next((d for d in depts if '원불교' in d['label']), None)
        assert won is not None
    finally:
        await crawler.stop()

@pytest.mark.asyncio
async def test_wonkwang_context_manager():
    # Context manager support
    async with WonkwangCrawler() as crawler:
        colleges = await crawler.get_colleges()
        assert isinstance(colleges, list)
        assert len(colleges) > 0

@pytest.mark.asyncio
async def test_scrape_timetable():
    async with WonkwangCrawler() as crawler:
        colleges = await crawler.get_colleges()
        # Find Kyohak College and Won Buddhism Dept
        kyohak = next((c for c in colleges if '교학' in c['label']), None)
        assert kyohak is not None
        
        depts = await crawler.get_departments(kyohak['value'])
        won = next((d for d in depts if '원불교' in d['label']), None)
        assert won is not None
        
        courses = await crawler.scrape_timetable(kyohak['value'], won['value'])
        assert isinstance(courses, list)
        # Won Buddhism usually has courses
        assert len(courses) > 0
        
        course = courses[0]
        assert "course_name" in course
        assert "code_lesson" in course
        assert "class_no" in course
        assert "employee_no" in course
        assert "professor" in course
        assert "syllabus_url" in course
        assert "lectRPlanView.jsp" in course["syllabus_url"]
        assert "codeLesson=" in course["syllabus_url"]

import asyncio
import json
import os
import re
from typing import List, Dict, Any, Optional
from playwright.async_api import async_playwright, Browser, BrowserContext, Page
from crawlers.base import BaseCrawler

class WonkwangCrawler(BaseCrawler):
    """원광대학교 강의계획서 크롤러"""
    
    BASE_URL = "https://intra.wku.ac.kr/SWupis/V005/Service/Stud/TimeTable/timeTableByDept.jsp?sm=2"
    SYLLABUS_BASE_URL = "https://intra.wku.ac.kr/SWupis/V005/Service/Teach/HLecPlan/lectRPlanView.jsp"
    
    def __init__(self, output_dir: str = "data/wonkwang"):
        super().__init__(university_name="원광대학교", base_url=self.BASE_URL)
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self._playwright = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    async def start(self):
        """브라우저 및 페이지 세션을 시작합니다."""
        if not self._playwright:
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(headless=True)
            self._context = await self._browser.new_context()
            self.page = await self._context.new_page()

    async def stop(self):
        """브라우저 및 세션을 종료합니다."""
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()
        self._playwright = None
        self._browser = None
        self._context = None
        self.page = None

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    async def get_colleges(self) -> List[Dict[str, str]]:
        """대학(College) 목록을 가져옵니다."""
        if not self.page:
            await self.start()
            
        try:
            await self.page.goto(self.BASE_URL)
            await self.page.wait_for_selector("select[name='college']")
            
            colleges = await self.page.eval_on_selector_all(
                "select[name='college'] option", 
                "options => options.map(o => ({label: o.innerText.trim(), value: o.value})).filter(o => o.value !== '')"
            )
            return colleges
        except Exception as e:
            print(f"Error in get_colleges: {e}")
            return []

    async def get_departments(self, college_value: str) -> List[Dict[str, str]]:
        """특정 대학의 학과(Department) 목록을 가져옵니다."""
        if not self.page:
            await self.start()
            
        try:
            if self.page.url != self.BASE_URL:
                await self.page.goto(self.BASE_URL)
            
            await self.page.wait_for_selector("select[name='college']")
            await self.page.select_option("select[name='college']", college_value)
            
            # 대학 선택 시 onchange로 submit()이 호출되어 페이지가 새로고침됩니다.
            await self.page.wait_for_load_state("networkidle")
            
            # 학과 목록이 채워질 때까지 대기
            await self.page.wait_for_function(
                "() => document.querySelector(\"select[name='codeRegiment']\").options.length > 1"
            )
            
            departments = await self.page.eval_on_selector_all(
                "select[name='codeRegiment'] option", 
                "options => options.map(o => ({label: o.innerText.trim(), value: o.value})).filter(o => o.value !== '')"
            )
            return departments
        except Exception as e:
            print(f"Error in get_departments: {e}")
            return []

    async def scrape_timetable(self, college_value: str, dept_value: str) -> List[Dict[str, Any]]:
        """학과별 시간표에서 강의 정보를 추출합니다."""
        if not self.page:
            await self.start()
            
        try:
            # 대학 및 학과 선택 (이미 선택되어 있을 수 있지만 안전을 위해 재설정)
            await self.page.select_option("select[name='college']", college_value)
            await self.page.wait_for_load_state("networkidle")
            # 2. 학과 선택
            print(f"DEBUG: Selecting department {dept_value}")
            await self.page.select_option("select[name='codeRegiment']", dept_value)
            await self.page.wait_for_load_state("networkidle")

            # 3. '시간표 조회' 버튼 클릭 (이미 제출되었을 수도 있지만 확실히 하기 위해 클릭)
            print(f"DEBUG: Clicking search button")
            # 버튼이 사라졌을 수도 있으므로 존재 여부 확인 후 클릭
            search_button = await self.page.query_selector("input[value='시간표 조회']")
            if search_button:
                await search_button.click()
                await self.page.wait_for_load_state("networkidle")
            else:
                print("DEBUG: Search button not found, it might have been submitted by onchange")

            
            # 테이블 데이터 대기
            print("DEBUG: Waiting for table rows")
            try:
                await self.page.wait_for_selector("table.table-bordered tr", timeout=5000)
            except Exception as e:
                print(f"DEBUG: Timeout waiting for table rows: {e}")
                return []
            
            # 헤더 인덱스 찾기
            header_cells = await self.page.query_selector_all("table.table-bordered th")
            if not header_cells:
                # 첫 번째 행이 th를 포함하지 않는 경우 첫 번째 tr의 td를 확인
                first_row_cells = await self.page.query_selector_all("table.table-bordered tr:first-child td")
                header_cells = first_row_cells
            
            header_texts = [(await c.inner_text()).strip() for c in header_cells]
            print(f"DEBUG: Header texts: {header_texts}")
            
            col_map = {}
            for idx, text in enumerate(header_texts):
                if "과목명" in text: col_map["name"] = idx
                elif "교수" in text: col_map["professor"] = idx
                elif "과목번호" in text or "교과목번호" in text: col_map["code"] = idx
                elif "분반" in text: col_map["class"] = idx
            
            print(f"DEBUG: Column map: {col_map}")

            rows = await self.page.query_selector_all("table.table-bordered tr")
            courses = []
            
            for i, row in enumerate(rows):
                cells = await row.query_selector_all("td")
                if len(cells) < 4: # 최소한의 데이터가 있어야 함
                    continue
                
                texts = [(await c.inner_text()).strip() for c in cells]
                
                # 과목명 링크 및 URL 분석
                link_element = None
                name_idx = col_map.get("name", 3)
                if name_idx < len(cells):
                    link_element = await cells[name_idx].query_selector("a")
                
                if not link_element:
                    # 모든 셀에서 링크 찾기 시도
                    for idx, cell in enumerate(cells):
                        link_element = await cell.query_selector("a")
                        if link_element:
                            name_idx = idx
                            break
                
                if not link_element:
                    continue
                
                course_name = texts[name_idx]
                
                # URL 추출 (onclick 또는 href)
                url_attr = await link_element.get_attribute("onclick")
                if not url_attr:
                    url_attr = await link_element.get_attribute("href")
                
                if url_attr:
                    # lectRPlanView.jsp 파라미터 추출
                    params_match = re.search(r"'(.*?)'", url_attr)
                    if params_match:
                        relative_url = params_match.group(1)
                        if "lectRPlanView.jsp" in relative_url:
                            if relative_url.startswith("/"):
                                syllabus_url = f"https://intra.wku.ac.kr{relative_url}"
                            else:
                                syllabus_url = f"https://intra.wku.ac.kr/SWupis/V005/Service/Teach/HLecPlan/{relative_url}"
                            
                            code_lesson = ""
                            class_no = ""
                            employee_no = ""
                            
                            code_match = re.search(r"codeLesson=([^&]*)", relative_url)
                            class_match = re.search(r"classNo=([^&]*)", relative_url)
                            emp_match = re.search(r"employeeNo=([^&]*)", relative_url)
                            
                            if code_match: code_lesson = code_match.group(1)
                            if class_match: class_no = class_match.group(1)
                            if emp_match: employee_no = emp_match.group(1)
                            
                            professor = texts[col_map.get("professor")] if "professor" in col_map and col_map["professor"] < len(texts) else ""
                            
                            courses.append({
                                "course_name": course_name,
                                "code_lesson": code_lesson,
                                "class_no": class_no,
                                "employee_no": employee_no,
                                "professor": professor,
                                "syllabus_url": syllabus_url
                            })
            
            return courses
        except Exception as e:
            print(f"Error in scrape_timetable: {e}")
            return []

    async def scrape_syllabus(self, syllabus_url: str) -> Dict[str, Any]:
        """강의계획서 상세 정보를 추출합니다."""
        if not self.page:
            await self.start()
            
        try:
            await self.page.goto(syllabus_url)
            await self.page.wait_for_load_state("networkidle")
            
            # 강의목표 추출
            objective = await self.page.evaluate("""() => {
                const ths = Array.from(document.querySelectorAll('th.h_char'));
                const goalTh = ths.find(th => th.innerText.includes('교과목 목표'));
                if (goalTh) {
                    const nextTh = goalTh.nextElementSibling;
                    return nextTh ? nextTh.innerText.trim() : "";
                }
                return "";
            }""")
            
            # 강의개요 추출
            overview = await self.page.evaluate("""() => {
                const ths = Array.from(document.querySelectorAll('th.h_char'));
                const natureTh = ths.find(th => th.innerText.includes('교과목 성격'));
                if (natureTh) {
                    const nextTh = natureTh.nextElementSibling;
                    return nextTh ? nextTh.innerText.trim() : "";
                }
                return "";
            }""")
            
            # 평가 방법 추출
            evaluation = await self.page.evaluate("""() => {
                const tables = Array.from(document.querySelectorAll('table.tbl_bbs'));
                const evalTable = tables.find(t => t.innerText.includes('성적평가방법'));
                if (evalTable) {
                    const rows = evalTable.querySelectorAll('tr');
                    if (rows.length >= 3) {
                        const labels = Array.from(rows[1].querySelectorAll('th')).map(th => th.innerText.trim());
                        const values = Array.from(rows[2].querySelectorAll('th')).map(th => th.innerText.trim());
                        return labels.map((l, i) => `${l}: ${values[i] || "0"}`).join(', ');
                    }
                }
                return "";
            }""")
            
            # 주별 계획 추출
            weekly_plan = await self.page.evaluate("""() => {
                const h4s = Array.from(document.querySelectorAll('h4.h_title_h3'));
                const weeklyH4 = h4s.find(h => h.innerText.includes('주별 세부내용'));
                if (weeklyH4) {
                    const table = weeklyH4.nextElementSibling.nextElementSibling; // p 다음에 table
                    if (table && table.tagName === 'TABLE') {
                        const rows = Array.from(table.querySelectorAll('tbody tr'));
                        return rows.map(row => {
                            const cells = row.querySelectorAll('td');
                            if (cells.length >= 3) {
                                return {
                                    week: cells[0].innerText.trim(),
                                    topic: cells[1].innerText.trim(),
                                    content: cells[2].innerText.trim()
                                };
                            }
                            return null;
                        }).filter(x => x !== null);
                    }
                }
                return [];
            }""")
            
            return {
                "objective": objective,
                "overview": overview,
                "evaluation": evaluation,
                "weekly_plan": weekly_plan
            }
        except Exception as e:
            print(f"Error in scrape_syllabus: {e}")
            return {"objective": "", "overview": "", "evaluation": "", "weekly_plan": []}

    async def run(self):
        """원광대학교 전체 강의계획서 크롤링 메인 로직"""
        async with self as crawler:
            colleges = await crawler.get_colleges()
            for college in colleges:
                print(f"[*] 대학 크롤링 중: {college['label']}")
                departments = await crawler.get_departments(college['value'])
                for dept in departments:
                    print(f"  [-] 학과 크롤링 중: {dept['label']}")
                    courses = await crawler.scrape_timetable(college['value'], dept['value'])
                    for course in courses:
                        print(f"    [+] 강의 상세 수집 중: {course['course_name']}")
                        details = await crawler.scrape_syllabus(course['syllabus_url'])
                        self.add_lecture(
                            title=course['course_name'],
                            professor=course['professor'],
                            department=dept['label'],
                            objective=details['objective'],
                            url=course['syllabus_url']
                        )
            self.save_results()

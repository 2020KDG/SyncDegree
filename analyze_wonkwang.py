import asyncio
from playwright.async_api import async_playwright

async def analyze_wonkwang():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 1. 시간표 조회 페이지 접속
        url = "https://intra.wku.ac.kr/SWupis/V005/Service/Stud/TimeTable/timeTableByDept.jsp?sm=2"
        print(f"Connecting to {url}...")
        await page.goto(url)
        await page.wait_for_load_state("networkidle")

        # 2. 대학(College) 셀렉트 박스 분석
        try:
            await page.wait_for_selector("select[name='codeCollege']", timeout=10000)
            colleges = await page.eval_on_selector_all("select[name='codeCollege'] option", "options => options.map(o => ({label: o.innerText.trim(), value: o.value}))")
            print("\n[Colleges]")
            for c in colleges:
                print(f"- {c['label']}: {c['value']}")
        except Exception as e:
            print(f"Error finding college select: {e}")
            print(await page.content())
            return

        # 3. '교학대학' 선택 시도 (Value: 0001 가정 또는 검색)
        kyohak = next((c for c in colleges if '교학' in c['label']), None)
        if kyohak:
            print(f"\nSelecting College: {kyohak['label']} ({kyohak['value']})")
            await page.select_option("select[name='codeCollege']", kyohak['value'])
            await page.wait_for_timeout(1000) # 학과 목록 로딩 대기

            # 4. 학과(Department) 셀렉트 박스 분석
            depts = await page.eval_on_selector_all("select[name='codeDept'] option", "options => options.map(o => ({label: o.innerText.trim(), value: o.value}))")
            print("\n[Departments in Kyohak]")
            for d in depts[:5]:
                print(f"- {d['label']}: {d['value']}")

            # 5. '원불교학과' 선택
            won = next((d for d in depts if '원불교' in d['label']), None)
            if won:
                print(f"Selecting Dept: {won['label']} ({won['value']})")
                await page.select_option("select[name='codeDept']", won['value'])
                
                # 6. 조회 버튼 클릭 (버튼 셀렉터 확인 필요, 보통 <a>나 <button> 또는 input[type=button])
                # 페이지 소스를 보지 못했으므로 텍스트로 찾거나 기본 버튼 클릭 시도
                search_btn = await page.get_by_text("시간표 조회").first
                if await search_btn.is_visible():
                    print("Clicking Search Button...")
                    await search_btn.click()
                    await page.wait_for_timeout(2000)

                    # 7. 강의 목록 테이블 분석
                    # 강의명 클릭 시 실행되는 자바스크립트 함수 추출 시도
                    # 보통 onclick="doView('...', '...')" 형태
                    rows = await page.query_selector_all("table tr")
                    print(f"\nFound {len(rows)} rows in timetable.")
                    
                    # 샘플 행에서 onclick 속성 확인
                    for row in rows[:10]:
                        links = await row.query_selector_all("a")
                        for link in links:
                            text = await link.inner_text()
                            onclick = await link.get_attribute("onclick")
                            if onclick:
                                print(f"Link: {text.strip()} | OnClick: {onclick}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(analyze_wonkwang())

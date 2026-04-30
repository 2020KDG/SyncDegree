# Wonkwang Crawler Fixes and Improvements Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix critical bugs in Wonkwang University crawler, implement syllabus detail extraction, and robust orchestration.

**Architecture:** 
1. Fix `SyntaxError` and `AttributeError` in `WonkwangCrawler`.
2. Implement robust table parsing by finding column indices via `<th>` headers.
3. Implement `scrape_syllabus` to extract detailed course information from the popup.
4. Update `run()` to orchestrate the full scraping process and save to JSON.

**Tech Stack:** Python, Playwright, Pytest

---

### Task 1: Fix Syntax and Initialization Errors

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Fix SyntaxError in `scrape_timetable`**
Replace the multi-line string in `page.evaluate` with a single-line string or triple quotes.

- [ ] **Step 2: Fix AttributeError in `start()`**
Correct the initialization of `self._browser`.

- [ ] **Step 3: Verify the fix with reproduction script**
Run `python reproduce_bugs.py` and ensure it passes the initialization phase (it might still fail at `scrape_timetable` due to hardcoded indices, but `SyntaxError` and `AttributeError` should be gone).

### Task 2: Implement Robust Table Parsing

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Update `scrape_timetable` to find column indices**
Extract indices for "과목명", "담당교수", "분반", "교과목번호", etc. from the `<thead>` or first `<tr>` containing `<th>`.

- [ ] **Step 2: Use discovered indices to extract course data**
Replace hardcoded `texts[6]` and other indices with the discovered ones.

- [ ] **Step 3: Verify with `pytest tests/test_wonkwang_crawler.py`**
Run: `pytest tests/test_wonkwang_crawler.py::test_scrape_timetable -v`

### Task 3: Implement Syllabus Detail Extraction

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Implement `scrape_syllabus(syllabus_url)`**
```python
async def scrape_syllabus(self, syllabus_url: str) -> Dict[str, Any]:
    # Navigate to syllabus_url
    # Wait for table
    # Extract Course Goals, Overview, Evaluation, Weekly Schedule
    # Return dict
```

- [ ] **Step 2: Create a test for `scrape_syllabus`**
Add a test case in a new test file or `tests/test_wonkwang_crawler.py`.

- [ ] **Step 3: Run the test to verify**
Run: `pytest tests/test_wonkwang_crawler.py -v`

### Task 4: Orchestration and Data Persistence

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Update `run()` method**
Integrate `scrape_timetable` and `scrape_syllabus`.

- [ ] **Step 2: Implement JSON saving**
Ensure results are saved to `data/wonkwang.json`.

- [ ] **Step 3: Create a small sample run script**
Verify one department's syllabus extraction.

- [ ] **Step 4: Run all tests**
Run: `pytest tests/test_wonkwang_crawler.py -v`

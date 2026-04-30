# Wonkwang University Crawler Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a crawler for Wonkwang University syllabus data using Playwright.

**Architecture:** A standalone crawler class `WonkwangCrawler` in `crawlers/wonkwang.py` that inherits from a base crawler (if exists) or follows the project's established pattern. It will perform a nested crawl: Colleges -> Departments -> Courses -> Syllabus Details.

**Tech Stack:** Python, Playwright, BeautifulSoup4 (for parsing static HTML), JSON.

---

### Task 1: Setup Crawler Structure

**Files:**
- Create: `crawlers/wonkwang.py`

- [ ] **Step 1: Define the `WonkwangCrawler` class with basic configuration**

```python
import asyncio
import json
import os
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

class WonkwangCrawler:
    BASE_URL = "https://intra.wku.ac.kr/SWupis/V005/Service/Stud/TimeTable/timeTableByDept.jsp?sm=2"
    SYLLABUS_BASE_URL = "https://intra.wku.ac.kr/SWupis/V005/Service/Teach/HLecPlan/lectRPlanView.jsp"
    
    def __init__(self, output_dir="data/wonkwang"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
```

- [ ] **Step 2: Implement `get_colleges` method**
- [ ] **Step 3: Implement `get_departments` method**

### Task 2: Implement Course List Extraction

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Implement `scrape_timetable` method**
  - Select college and department.
  - Click "시간표 조회" (or trigger search).
  - Parse the table to get course IDs and syllabus link parameters.

### Task 3: Implement Syllabus Detail Extraction

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Implement `scrape_syllabus` method**
  - Navigate to the syllabus URL.
  - Extract: Course Name, Professor, Goals, Evaluation Criteria, etc.

### Task 4: Orchestration and Data Persistence

**Files:**
- Modify: `crawlers/wonkwang.py`

- [ ] **Step 1: Implement `run` method to tie everything together**
- [ ] **Step 2: Add JSON saving logic**

### Task 5: Verification

- [ ] **Step 1: Create a test script to run the crawler for a single department**
- [ ] **Step 2: Verify the output JSON structure**

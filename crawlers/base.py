import abc
import json
import os
from typing import List, Dict

class BaseCrawler(abc.ABC):
    def __init__(self, university_name: str, base_url: str):
        self.university_name = university_name
        self.base_url = base_url
        self.results = []

    @abc.abstractmethod
    async def run(self):
        """실제 크롤링 로직을 구현하는 메서드"""
        pass

    def save_results(self):
        """결과를 data 폴더에 JSON으로 저장"""
        os.makedirs("data", exist_ok=True)
        file_path = f"data/{self.university_name}.json"
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"[*] {self.university_name} 데이터 저장 완료: {file_path}")

    def add_lecture(self, title: str, professor: str, department: str, objective: str, url: str):
        """강의 데이터를 리스트에 추가"""
        self.results.append({
            "university": self.university_name,
            "course_title": title,
            "professor": professor,
            "department": department,
            "learning_objective": objective,
            "syllabus_url": url
        })

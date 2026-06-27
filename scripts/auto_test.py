"""
word-game 자동 테스트 스크립트
모든 변경 후 자동 실행됨
"""

import os
import json
import subprocess
import sys
from pathlib import Path


class AutoTester:
    """자동 테스트 클래스"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.results = []
        self.errors = []
    
    def log(self, test_name: str, passed: bool, message: str = ""):
        """결과 로깅"""
        status = "PASS" if passed else "FAIL"
        self.results.append({"test": test_name, "passed": passed, "message": message})
        print(f"[{status}] {test_name}: {message}")
    
    def test_file_structure(self):
        """파일 구조 검증"""
        required_files = [
            "index.html",
            "css/style.css",
            "js/game.js",
            "data/questions.json",
            "AGENTS.md",
            "DESIGN.MD",
            "LAWDB.MD",
            ".gitignore"
        ]
        
        for file in required_files:
            path = self.project_root / file
            if path.exists():
                self.log(f"파일 존재: {file}", True)
            else:
                self.log(f"파일 존재: {file}", False, "파일 없음")
    
    def test_html_structure(self):
        """HTML 구조 검증"""
        html_file = self.project_root / "index.html"
        
        if not html_file.exists():
            self.log("HTML 검증", False, "index.html 없음")
            return
        
        content = html_file.read_text(encoding="utf-8")
        
        checks = [
            ("DOCTYPE 선언", "<!DOCTYPE html>" in content),
            ("lang 속성", 'lang="ko"' in content),
            ("title 태그", "<title>" in content),
            ("charset 선언", 'charset="UTF-8"' in content),
            ("사이드바 존재", 'class="sidebar"' in content),
            ("게임 영역 존재", 'class="game-area"' in content)
        ]
        
        for name, passed in checks:
            self.log(f"HTML: {name}", passed)
    
    def test_css_syntax(self):
        """CSS 문법 검증"""
        css_file = self.project_root / "css/style.css"
        
        if not css_file.exists():
            self.log("CSS 검증", False, "style.css 없음")
            return
        
        content = css_file.read_text(encoding="utf-8")
        
        # 기본 문법 검증
        checks = [
            ("중괄호 매칭", content.count("{") == content.count("}")),
            ("세미콜론 존재", ";" in content),
            ("클래스 정의 존재", "." in content)
        ]
        
        for name, passed in checks:
            self.log(f"CSS: {name}", passed)
    
    def test_js_syntax(self):
        """JS 문법 검증"""
        js_file = self.project_root / "js/game.js"
        
        if not js_file.exists():
            self.log("JS 검증", False, "game.js 없음")
            return
        
        content = js_file.read_text(encoding="utf-8")
        
        checks = [
            ("괄호 매칭", content.count("{") == content.count("}")),
            ("괄호 매칭", content.count("(") == content.count(")")),
            ("세미콜론 존재", ";" in content),
            ("함수 정의 존재", "function " in content)
        ]
        
        for name, passed in checks:
            self.log(f"JS: {name}", passed)
    
    def test_json_validity(self):
        """JSON 유효성 검증"""
        json_file = self.project_root / "data/questions.json"
        
        if not json_file.exists():
            self.log("JSON 검증", False, "questions.json 없음")
            return
        
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.log("JSON 파싱", True)
            
            # 주제 존재 검증
            required_topics = ["civil", "admin", "criminal", "criminal-procedure", "commercial", "labor", "constitution"]
            for topic in required_topics:
                if topic in data:
                    self.log(f"주제 존재: {topic}", True)
                else:
                    self.log(f"주제 존재: {topic}", False, "주제 없음")
            
            # 각 주제의 문제 구조 검증
            for topic, content in data.items():
                if "ox" in content and "blank" in content:
                    self.log(f"문제 구조: {topic}", True)
                else:
                    self.log(f"문제 구조: {topic}", False, "ox 또는 blank 없음")
        
        except json.JSONDecodeError as e:
            self.log("JSON 파싱", False, f"JSON 문법 오류: {e}")
    
    def test_git_status(self):
        """Git 상태 검증"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                cwd=self.project_root
            )
            
            if result.returncode == 0:
                if result.stdout.strip():
                    self.log("Git 상태", True, "변경사항 있음")
                else:
                    self.log("Git 상태", True, "변경사항 없음")
            else:
                self.log("Git 상태", False, "Git 오류")
        
        except FileNotFoundError:
            self.log("Git 상태", False, "Git 미설치")
    
    def test_db_schema(self):
        """DB 스키마 검증"""
        schema_file = self.project_root / "db/schema.sql"
        
        if schema_file.exists():
            content = schema_file.read_text(encoding="utf-8")
            
            checks = [
                ("subjects 테이블", "CREATE TABLE" in content and "subjects" in content),
                ("keywords 테이블", "keywords" in content),
                ("questions 테이블", "questions" in content)
            ]
            
            for name, passed in checks:
                self.log(f"DB 스키마: {name}", passed)
        else:
            self.log("DB 스키마", False, "schema.sql 없음")
    
    def run_all_tests(self):
        """모든 테스트 실행"""
        print("=" * 50)
        print("word-game 자동 테스트 시작")
        print("=" * 50)
        
        self.test_file_structure()
        self.test_html_structure()
        self.test_css_syntax()
        self.test_js_syntax()
        self.test_json_validity()
        self.test_git_status()
        self.test_db_schema()
        
        # 결과 요약
        passed = sum(1 for r in self.results if r["passed"])
        failed = sum(1 for r in self.results if not r["passed"])
        total = len(self.results)
        
        print("=" * 50)
        print(f"테스트 결과: {passed}/{total} 통과")
        if failed > 0:
            print(f"실패: {failed}개")
        print("=" * 50)
        
        return failed == 0


def main():
    """메인 함수"""
    tester = AutoTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

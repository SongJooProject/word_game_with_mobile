import json

print("=" * 60)
print("셀프테스트")
print("=" * 60)

# 1. JSON 파일 확인
print("\n[1] JSON 파일 구조 확인")
with open("data/questions.json", "r", encoding="utf-8") as f:
    data = json.load(f)

assert "subjects" in data, "subjects 키 없음"
assert len(data["subjects"]) > 0, "과목 없음"

subject = data["subjects"][0]
assert subject["name"] == "형사소송법", "과목명 오류"
assert "chapters" in subject, "chapters 없음"

total_questions = 0
for ch in subject["chapters"]:
    assert "name" in ch, f"챕터 이름 없음"
    assert "questions" in ch, f"챕터 문제 없음"
    total_questions += len(ch["questions"])
    
    for q in ch["questions"]:
        assert "type" in q, "문제 타입 없음"
        assert "question" in q, "문제 내용 없음"
        assert q["type"] in ["type1", "type2"], f"잘못된 타입: {q['type']}"
        
        if q["type"] == "type1":
            assert "options" in q, "선택지 없음"
            assert "answer" in q, "정답 없음"
            assert 1 <= q["answer"] <= len(q["options"]), f"정답 범위 오류: {q['answer']}"
        else:
            assert "answer" in q, "빈칸 정답 없음"

print(f"  과목: {subject['name']}")
print(f"  챕터: {len(subject['chapters'])}개")
print(f"  전체 문제: {total_questions}개")
print(f"  OK JSON 구조 정상")

# 2. HTML 파일 확인
print("\n[2] HTML 파일 확인")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

checks = [
    ("breadcrumb", "빵 부스러기"),
    ("menu-level-chapter", "챕터 메뉴"),
    ("menu-level-section", "섹션 메뉴"),
    ("game-type-selector", "게임 유형 선택"),
    ("type1", "선택형 버튼"),
    ("type2", "빈칸형 버튼"),
    ("all", "전체 버튼"),
    ("btn-start", "시작 버튼"),
    ("btn-back", "뒤로 버튼"),
]

for check_id, desc in checks:
    assert check_id in html, f"{desc} 누락: {check_id}"
    print(f"  OK {desc}")

# 3. JS 파일 확인
print("\n[3] JavaScript 파일 확인")
with open("js/game.js", "r", encoding="utf-8") as f:
    js = f.read()

js_checks = [
    ("renderSubjectList", "과목 목록 렌더링"),
    ("selectSubject", "과목 선택"),
    ("renderChapterList", "챕터 목록 렌더링"),
    ("selectChapter", "챕터 선택"),
    ("renderSectionList", "섹션 목록 렌더링"),
    ("selectSection", "섹션 선택"),
    ("selectGameType", "게임 유형 선택"),
    ("startGame", "게임 시작"),
    ("showQuestion", "문제 표시"),
    ("checkType1Answer", "선택형 답 확인"),
    ("checkAnswer", "빈칸형 답 확인"),
    ("nextQuestion", "다음 문제"),
    ("goBack", "뒤로 가기"),
    ("navigationState", "네비게이션 상태"),
]

for func_name, desc in js_checks:
    assert func_name in js, f"{desc} 함수 누락: {func_name}"
    print(f"  OK {desc}")

# 4. CSS 파일 확인
print("\n[4] CSS 파일 확인")
with open("css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

css_checks = [
    ("breadcrumb", "빵 부스러기 스타일"),
    ("menu-level", "메뉴 레벨 스타일"),
    ("menu-item", "메뉴 아이템 스타일"),
    ("option-btn", "선택형 버튼 스타일"),
    ("chapter-item", "챕터 아이템 스타일"),
    ("section-item", "섹션 아이템 스타일"),
]

for check_class, desc in css_checks:
    assert check_class in css, f"{desc} 누락: {check_class}"
    print(f"  OK {desc}")

# 5. 서버 접근 확인
print("\n[5] 서버 접근 확인")
import urllib.request
try:
    response = urllib.request.urlopen("http://localhost:8000/")
    assert response.status == 200, f"메인 페이지 오류: {response.status}"
    print("  OK 메인 페이지 접근 가능")
    
    response = urllib.request.urlopen("http://localhost:8000/data/questions.json")
    assert response.status == 200, f"JSON 파일 오류: {response.status}"
    print("  OK JSON 파일 접근 가능")
    
    response = urllib.request.urlopen("http://localhost:8000/js/game.js")
    assert response.status == 200, f"JS 파일 오류: {response.status}"
    print("  OK JS 파일 접근 가능")
    
    response = urllib.request.urlopen("http://localhost:8000/css/style.css")
    assert response.status == 200, f"CSS 파일 오류: {response.status}"
    print("  OK CSS 파일 접근 가능")
except Exception as e:
    print(f"  FAIL 서버 접근 실패: {e}")

print("\n" + "=" * 60)
print("셀프테스트 완료!")
print("=" * 60)

"""
엑셀 문제 데이터를 JSON으로 변환하는 스크립트
"""

import openpyxl
import json
import re
from pathlib import Path


def parse_excel_to_questions(excel_path):
    """엑셀 파일을 읽어 문제 데이터로 변환"""
    wb = openpyxl.load_workbook(excel_path, data_only=True)

    all_chapters = []

    for sheet_name in wb.sheetnames:
        if sheet_name == "Sheet1":
            continue  # 설명 시트는 스킵

        ws = wb[sheet_name]
        questions = []
        current_section = ""

        for row in ws.iter_rows(min_row=1, max_row=ws.max_row, values_only=True):
            cells = [str(cell) if cell is not None else "" for cell in row]

            # B열이 비어있으면 스킵
            if len(cells) < 3 or cells[1] == "":
                # 소제목 확인
                if cells[2] and cells[2].strip():
                    current_section = cells[2].strip()
                continue

            q_type = cells[1].strip()
            content = cells[2].strip() if len(cells) > 2 else ""

            if not content:
                continue

            if q_type == "type1":
                # 선택형 문제
                options = []
                for i in range(3, 9):  # D~I열
                    if i < len(cells) and cells[i].strip():
                        options.append(cells[i].strip())

                answer = cells[10].strip() if len(cells) > 10 else ""  # K열

                if options and answer:
                    questions.append({
                        "type": "type1",
                        "section": current_section,
                        "question": content,
                        "options": options,
                        "answer": int(answer) if answer.isdigit() else 1
                    })

            elif q_type == "type2":
                # 빈칸형 문제
                # < > 안의 내용이 정답
                blanks = re.findall(r'<([^>]+)>', content)
                answer = blanks[0] if blanks else ""

                questions.append({
                    "type": "type2",
                    "section": current_section,
                    "question": content,
                    "answer": answer
                })

        if questions:
            all_chapters.append({
                "name": sheet_name,
                "questions": questions
            })

    return all_chapters


def main():
    excel_path = Path("db/DB....xlsx")
    output_path = Path("data/questions.json")

    print("=" * 50)
    print("엑셀 → JSON 변환")
    print("=" * 50)

    chapters = parse_excel_to_questions(excel_path)

    # 기존 데이터와 합치기
    if output_path.exists():
        with open(output_path, "r", encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {"subjects": []}

    # 형사소송법 데이터 찾기 또는 추가
    subject_data = None
    for subj in existing.get("subjects", []):
        if subj.get("name") == "형사소송법":
            subject_data = subj
            break

    if not subject_data:
        subject_data = {"name": "형사소송법", "chapters": []}
        existing.setdefault("subjects", []).append(subject_data)

    subject_data["chapters"] = chapters

    # 저장
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(existing, f, ensure_ascii=False, indent=2)

    # 통계
    total_q = sum(len(ch["questions"]) for ch in chapters)
    print("\n변환 완료!")
    print(f"  - 시트(챕터): {len(chapters)}개")
    print(f"  - 전체 문제: {total_q}개")

    for ch in chapters:
        print(f"\n  [{ch['name']}]")
        type1_count = sum(1 for q in ch["questions"] if q["type"] == "type1")
        type2_count = sum(1 for q in ch["questions"] if q["type"] == "type2")
        print(f"    - 선택형: {type1_count}개")
        print(f"    - 빈칸형: {type2_count}개")

    print(f"\n저장: {output_path}")


if __name__ == "__main__":
    main()

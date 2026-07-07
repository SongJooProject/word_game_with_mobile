import json

with open("data/questions.json", "r", encoding="utf-8") as f:
    d = json.load(f)

# subjects만 추출
clean = {"subjects": d.get("subjects", [])}

with open("data/questions.json", "w", encoding="utf-8") as f:
    json.dump(clean, f, ensure_ascii=False, indent=2)

print("정리 완료!")
print(f"subjects: {len(clean['subjects'])}개")
for s in clean["subjects"]:
    total = sum(len(c["questions"]) for c in s["chapters"])
    print(f"  - {s['name']}: {total}문제")

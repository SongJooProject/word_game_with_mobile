import json

with open("data/questions.json", "r", encoding="utf-8") as f:
    d = json.load(f)

print("Top keys:", list(d.keys()))

subjects = d.get("subjects", [])
print("Subjects:", len(subjects))

for s in subjects:
    chapters = s.get("chapters", [])
    total = sum(len(c["questions"]) for c in chapters)
    type1 = sum(1 for c in chapters for q in c["questions"] if q["type"] == "type1")
    type2 = sum(1 for c in chapters for q in c["questions"] if q["type"] == "type2")
    print(f"\n  {s['name']}: {len(chapters)} chapters, {total} questions")
    print(f"    type1: {type1}, type2: {type2}")
    for c in chapters:
        print(f"    - {c['name']}: {len(c['questions'])} questions")

# Check game.js
with open("js/game.js", "r", encoding="utf-8") as f:
    js = f.read()

print("\n\n=== game.js checks ===")
print("getSubjectData:", "getSubjectData" in js)
print("getAllQuestions:", "getAllQuestions" in js)
print("checkType1Answer:", "checkType1Answer" in js)
print("type1:", "type1" in js)
print("type2:", "type2" in js)

# Check index.html
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

print("\n=== index.html checks ===")
print("criminal-procedure:", "criminal-procedure" in html)
print("selectGameType:", "selectGameType" in html)
print("type1 btn:", "type1" in html)
print("type2 btn:", "type2" in html)

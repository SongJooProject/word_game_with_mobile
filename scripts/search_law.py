import requests
import json

r = requests.get('http://www.law.go.kr/DRF/lawSearch.do', params={
    'OC': 'skagurwn',
    'target': 'law',
    'type': 'JSON',
    'query': '형사소송법',
    'display': 10
})
r.encoding = 'utf-8'
data = r.json()

laws = data.get('LawSearch', {}).get('law', [])
for law in laws:
    print(f"- {law.get('법령명_한글')}: MST={law.get('법령일련번호')}")

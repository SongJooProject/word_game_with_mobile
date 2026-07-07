import requests
import json

r = requests.get('http://www.law.go.kr/DRF/lawService.do', params={
    'OC': 'skagurwn', 
    'target': 'law', 
    'type': 'JSON', 
    'MST': '222287'
})
r.encoding = 'utf-8'
data = r.json()

with open('temp_law.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Saved to temp_law.json')

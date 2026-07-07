import requests

# 두 개의 MST로 법령 조회
for mst in ['222287', '280441']:
    r = requests.get('http://www.law.go.kr/DRF/lawService.do', params={
        'OC': 'skagurwn',
        'target': 'law',
        'type': 'JSON',
        'MST': mst
    })
    r.encoding = 'utf-8'
    data = r.json()

    law = data.get('법령', {})
    basic = law.get('기본정보', {})
    name = basic.get('법령명_한글', 'N/A')
    articles = law.get('조문', {}).get('조문단위', [])

    print(f"\n=== MST: {mst} ===")
    print(f"법령명: {name}")
    print(f"조문수: {len(articles)}개")
    if articles:
        first = articles[0]
        print(f"첫 조문: 제{first.get('조문번호')}조 - {first.get('조문제목', '')}")

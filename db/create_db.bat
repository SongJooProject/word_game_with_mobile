@echo off
echo 형사소송법 키워드 DB 생성 중...
python scripts/init_db.py
if %errorlevel% equ 0 (
    echo 완료: db/legal_terms.db
) else (
    echo 실패: Python 실행 오류
)
pause

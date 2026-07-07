"""
형사소송법 키워드 SQLite DB 관리
"""

import sqlite3
import json
import os


class LegalTermDB:
    """법령용어 SQLite DB 클래스"""

    def __init__(self, db_path: str = "db/legal_terms.db"):
        """
        초기화

        Args:
            db_path: DB 파일 경로
        """
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        """테이블 생성"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS subjects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                term TEXT NOT NULL,
                definition TEXT,
                source TEXT,
                is_verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        """)

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                subject_id INTEGER NOT NULL,
                question_type TEXT NOT NULL,
                content TEXT NOT NULL,
                answer TEXT NOT NULL,
                hint TEXT,
                is_verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (subject_id) REFERENCES subjects(id)
            )
        """)

        self.conn.commit()

    def add_subject(self, name: str, description: str = "") -> int:
        """
        주제 추가

        Args:
            name: 주제명 (예: 형사소송법)
            description: 설명

        Returns:
            주제 ID
        """
        self.cursor.execute(
            "INSERT OR IGNORE INTO subjects (name, description) VALUES (?, ?)",
            (name, description)
        )
        self.conn.commit()

        self.cursor.execute("SELECT id FROM subjects WHERE name = ?", (name,))
        return self.cursor.fetchone()[0]

    def add_keyword(
        self,
        subject_id: int,
        term: str,
        definition: str = "",
        source: str = "",
        is_verified: bool = False
    ) -> int:
        """
        키워드 추가

        Args:
            subject_id: 주제 ID
            term: 법률 용어
            definition: 정의
            source: 출처
            is_verified: 검수 여부

        Returns:
            키워드 ID
        """
        self.cursor.execute(
            """INSERT INTO keywords
               (subject_id, term, definition, source, is_verified)
               VALUES (?, ?, ?, ?, ?)""",
            (subject_id, term, definition, source, int(is_verified))
        )
        self.conn.commit()
        return self.cursor.lastrowid

    def add_keywords_batch(self, subject_id: int, keywords: list) -> int:
        """
        키워드 일괄 추가

        Args:
            subject_id: 주제 ID
            keywords: 키워드 목록 [{"term": "...", ...}]

        Returns:
            추가된 키워드 수
        """
        count = 0
        for kw in keywords:
            self.add_keyword(
                subject_id=subject_id,
                term=kw.get("term", ""),
                definition=kw.get("definition", ""),
                source=kw.get("source", ""),
                is_verified=kw.get("is_verified", False)
            )
            count += 1
        return count

    def get_keywords_by_subject(self, subject_name: str) -> list:
        """
        주제별 키워드 조회

        Args:
            subject_name: 주제명

        Returns:
            키워드 목록
        """
        self.cursor.execute("""
            SELECT k.id, k.term, k.definition, k.source, k.is_verified
            FROM keywords k
            JOIN subjects s ON k.subject_id = s.id
            WHERE s.name = ?
            ORDER BY k.term
        """, (subject_name,))

        return [
            {
                "id": row[0],
                "term": row[1],
                "definition": row[2],
                "source": row[3],
                "is_verified": bool(row[4])
            }
            for row in self.cursor.fetchall()
        ]

    def search_keywords(self, query: str) -> list:
        """
        키워드 검색

        Args:
            query: 검색어

        Returns:
            검색 결과
        """
        self.cursor.execute("""
            SELECT k.id, k.term, k.definition, s.name as subject
            FROM keywords k
            JOIN subjects s ON k.subject_id = s.id
            WHERE k.term LIKE ? OR k.definition LIKE ?
            ORDER BY k.term
        """, (f"%{query}%", f"%{query}%"))

        return [
            {
                "id": row[0],
                "term": row[1],
                "definition": row[2],
                "subject": row[3]
            }
            for row in self.cursor.fetchall()
        ]

    def export_to_json(self, subject_name: str, output_file: str):
        """
        주제별 키워드 JSON 내보내기

        Args:
            subject_name: 주제명
            output_file: 출력 파일 경로
        """
        keywords = self.get_keywords_by_subject(subject_name)

        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(keywords, f, ensure_ascii=False, indent=2)

        print(f"JSON 내보내기 완료: {output_file} ({len(keywords)}개)")

    def close(self):
        """DB 연결 종료"""
        self.conn.close()


def init_criminal_procedure():
    """형사소송법 초기 키워드 추가"""
    db = LegalTermDB()

    # 형사소송법 주제 추가
    subject_id = db.add_subject("형사소송법", "형사소송에 관한 법률")

    # 형사소송법 키워드
    keywords = [
        # 기본 개념
        {
            "term": "형사소송",
            "definition": "범죄에 대한 국가의 형벌권 실현을 위한 절차",
            "source": "형사소송법",
        },
        {
            "term": "피의자",
            "definition": "범죄의 혐의를 받고 있는 자",
            "source": "형사소송법",
        },
        {
            "term": "피고인",
            "definition": "기소되어 재판을 받는 자",
            "source": "형사소송법",
        },
        {
            "term": "고소인",
            "definition": "범죄로 인하여 피해를 입은 자가 수사기관에 신고하는 자",
            "source": "형사소송법",
        },
        {
            "term": "고발인",
            "definition": "범죄사실을 수사기관에 신고하는 자 (피해자 외)",
            "source": "형사소송법",
        },
        # 수사절차
        {
            "term": "수사",
            "definition": "범죄사실의 발견과 범인의 확인을 위한 국가의 활동",
            "source": "형사소송법",
        },
        {
            "term": "고소",
            "definition": "피해자가 수사기관에 범죄사실을 신고하는 행위",
            "source": "형사소송법",
        },
        {
            "term": "고발",
            "definition": "범죄사실을 수사기관에 신고하는 행위",
            "source": "형사소송법",
        },
        {
            "term": "진술거부권",
            "definition": "피의자가自己에 불리한 진술을 거부할 수 있는 권리",
            "source": "형사소송법",
        },
        {
            "term": "변호인",
            "definition": "피의자 또는 피고인을 방어하는 법률가",
            "source": "형사소송법",
        },
        # 체포·구속
        {
            "term": "체포",
            "definition": "피의자의 신체를 강제로 확보하는 처분",
            "source": "형사소송법",
        },
        {
            "term": "구속",
            "definition": "피의자 또는 피고인의 신체를 구금시설에 유치하는 처분",
            "source": "형사소송법",
        },
        {
            "term": "영장",
            "definition": "법원이 발부하는 수사 또는 강제처분의 허가서",
            "source": "형사소송법",
        },
        {
            "term": "체포영장",
            "definition": "법원이 발부하는 체포를 위한 영장",
            "source": "형사소송법",
        },
        {
            "term": "구속영장",
            "definition": "법원이 발부하는 구속을 위한 영장",
            "source": "형사소송법",
        },
        {
            "term": "영장주의",
            "definition": "신체 자유 침해 처분은 법원 영장이 있어야 하는 원칙",
            "source": "형사소송법",
        },
        # 기소
        {
            "term": "기소",
            "definition": "검사가 범죄사실을 법원에 보고하여 재판을 청구하는 행위",
            "source": "형사소송법",
        },
        {
            "term": "기소독점",
            "definition": "기소권은 검사에게만 있다는 원칙",
            "source": "형사소송법",
        },
        {
            "term": "공소장",
            "definition": "검사가 기소할 때 법원에 제출하는 서면",
            "source": "형사소송법",
        },
        {
            "term": "공소제기",
            "definition": "검사가 법원에 재판을 청구하는 행위",
            "source": "형사소송법",
        },
        # 재판절차
        {
            "term": "공판절차",
            "definition": "법원에서 범죄사실의 유무를 심리하는 절차",
            "source": "형사소송법",
        },
        {
            "term": "공판심리주의",
            "definition": "재판은 법정에서 직접 심리하여야 한다는 원칙",
            "source": "형사소송법",
        },
        {
            "term": "변론",
            "definition": "피고인 또는 변호인이 법원에서 의견을 진술하는 행위",
            "source": "형사소송법",
        },
        {
            "term": "선고",
            "definition": "법원이 판결을 공표하는 행위",
            "source": "형사소송법",
        },
        {
            "term": "판결",
            "definition": "법원이 범죄사실의 유무 및 형량을 결정하는 재판",
            "source": "형사소송법",
        },
        # 판결 유형
        {
            "term": "유죄판결",
            "definition": "피고인의 유죄를 인정하는 판결",
            "source": "형사소송법",
        },
        {
            "term": "무죄판결",
            "definition": "피고인의 무죄를 인정하는 판결",
            "source": "형사소송법",
        },
        {
            "term": "공소기각",
            "definition": "공소제기가 적법하지 아니할 때 재판을 종결하는 판결",
            "source": "형사소송법",
        },
        {
            "term": "면소",
            "definition": "형사소송의 조건을 결하여 재판을 종결하는 판결",
            "source": "형사소송법",
        },
        # 무죄추정
        {
            "term": "무죄추정원칙",
            "definition": "피고인은 유죄판결이 확정될 때까지 무죄로 추정된다는 원칙",
            "source": "형사소송법",
        },
        {
            "term": "검증",
            "definition": "범죄사실을 확인하기 위하여 증거를 조사하는 행위",
            "source": "형사소송법",
        },
        {
            "term": "증거",
            "definition": "범죄사실의 유무를 인정하는 데 사용되는 자료",
            "source": "형사소송법",
        },
        {
            "term": "자백",
            "definition": "피의자 또는 피고인이自己의 범죄사실을 인정하는 진술",
            "source": "형사소송법",
        },
        {
            "term": "진술",
            "definition": "피의자 또는 피고인이 범죄사실에 대하여 말하는 행위",
            "source": "형사소송법",
        },
        # 약식절차
        {
            "term": "약식절차",
            "definition": "경미한 범죄에 대하여 간이한 절차로 재판하는 제도",
            "source": "형사소송법",
        },
        {
            "term": "약식명령",
            "definition": "약식절차에 의하여 법원이 발하는 명령",
            "source": "형사소송법",
        },
        # 즉시항고
        {
            "term": "즉시항고",
            "definition": "결정에 대하여 즉시 법원에 불복을 신청하는 제도",
            "source": "형사소송법",
        },
        {
            "term": "항소",
            "definition": "판결에 대하여 상급 법원에 불복을 신청하는 제도",
            "source": "형사소송법",
        },
        {
            "term": "상고",
            "definition": "항소심 판결에 대하여 대법원에 불복을 신청하는 제도",
            "source": "형사소송법",
        },
        # 공소시효
        {
            "term": "공소시효",
            "definition": "일정한 기간이 경과하면 공소제기를 할 수 없는 제도",
            "source": "형사소송법",
        },
        # 형 집행
        {
            "term": "형의 집행",
            "definition": "유죄판결이 확정된 후 형을 실현하는 절차",
            "source": "형사소송법",
        },
        {
            "term": "집행유예",
            "definition": "일정 기간 형의 집행을 유예하는 제도",
            "source": "형사소송법",
        },
        {
            "term": "선고유예",
            "definition": "일정 기간 형의 선고를 유예하는 제도",
            "source": "형사소송법",
        },
    ]

    db.add_keywords_batch(subject_id, keywords)
    print(f"형사소송법 키워드 {len(keywords)}개 추가 완료")

    db.close()


if __name__ == "__main__":
    init_criminal_procedure()

-- 형사소송법 키워드 SQLite DB

-- 주제 테이블
CREATE TABLE IF NOT EXISTS subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 키워드 테이블
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    term TEXT NOT NULL,
    definition TEXT,
    source TEXT,
    is_verified INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
);

-- 문제 테이블
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
);

-- 형사소송법 주제 추가
INSERT OR IGNORE INTO subjects (name, description) VALUES 
('형사소송법', '형사소송에 관한 법률');

-- 형사소송법 키워드 추가
INSERT INTO keywords (subject_id, term, definition, source, is_verified) 
SELECT s.id, k.term, k.definition, k.source, 1
FROM subjects s
CROSS JOIN (
    SELECT '형사소송' as term, '범죄에 대한 국가의 형벌권 실현을 위한 절차' as definition, '형사소송법' as source
    UNION ALL SELECT '피의자', '범죄의 혐의를 받고 있는 자', '형사소송법'
    UNION ALL SELECT '피고인', '기소되어 재판을 받는 자', '형사소송법'
    UNION ALL SELECT '수사', '범죄사실의 발견과 범인의 확인을 위한 국가의 활동', '형사소송법'
    UNION ALL SELECT '기소', '검사가 범죄사실을 법원에 보고하여 재판을 청구하는 행위', '형사소송법'
    UNION ALL SELECT '체포', '피의자의 신체를 강제로 확보하는 처분', '형사소송법'
    UNION ALL SELECT '구속', '피의자 또는 피고인의 신체를 구금시설에 유치하는 처분', '형사소송법'
    UNION ALL SELECT '영장', '법원이 발부하는 수사 또는 강제처분의 허가서', '형사소송법'
    UNION ALL SELECT '영장주의', '체포·구속 등 신체의 자유를 침해하는 처분은 법원의 영장이 있어야 한다는 원칙', '형사소송법'
    UNION ALL SELECT '진술거부권', '피의자가自己에 불리한 진술을 거부할 수 있는 권리', '형사소송법'
    UNION ALL SELECT '변호인', '피의자 또는 피고인을 방어하는 법률가', '형사소송법'
    UNION ALL SELECT '공판절차', '법원에서 범죄사실의 유무를 심리하는 절차', '형사소송법'
    UNION ALL SELECT '공판심리주의', '재판은 법정에서 직접 심리하여야 한다는 원칙', '형사소송법'
    UNION ALL SELECT '무죄추정원칙', '피고인은 유죄판결이 확정될 때까지 무죄로 추정된다는 원칙', '형사소송법'
    UNION ALL SELECT '공소시효', '일정한 기간이 경과하면 공소제기를 할 수 없는 제도', '형사소송법'
    UNION ALL SELECT '항소', '판결에 대하여 상급 법원에 불복을 신청하는 제도', '형사소송법'
    UNION ALL SELECT '상고', '항소심 판결에 대하여 대법원에 불복을 신청하는 제도', '형사소송법'
    UNION ALL SELECT '약식절차', '경미한 범죄에 대하여 간이한 절차로 재판하는 제도', '형사소송법'
    UNION ALL SELECT '즉시항고', '결정에 대하여 즉시 법원에 불복을 신청하는 제도', '형사소송법'
    UNION ALL SELECT '검증', '범죄사실을 확인하기 위하여 증거를 조사하는 행위', '형사소송법'
    UNION ALL SELECT '증거', '범죄사실의 유무를 인정하는 데 사용되는 자료', '형사소송법'
    UNION ALL SELECT '자백', '피의자 또는 피고인이自己의 범죄사실을 인정하는 진술', '형사소송법'
    UNION ALL SELECT '판결', '법원이 범죄사실의 유무 및 형량을 결정하는 재판', '형사소송법'
    UNION ALL SELECT '유죄판결', '피고인의 유죄를 인정하는 판결', '형사소송법'
    UNION ALL SELECT '무죄판결', '피고인의 무죄를 인정하는 판결', '형사소송법'
) k
WHERE s.name = '형사소송법';

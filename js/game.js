// 상태 관리
let currentSubject = null;
let currentChapter = null;
let currentSection = null;
let gameType = 'all';
let questions = [];
let currentQuestion = 0;
let score = 0;
let correctAnswers = 0;
let wrongAnswers = 0;
let startTime = null;
let timerInterval = null;

// 네비게이션 상태
let navigationState = 'subject'; // subject, chapter, section, game

// 초기화
window.addEventListener('load', async () => {
    await loadQuestions();
    renderSubjectList();
});

// 과목 목록 렌더링
function renderSubjectList() {
    const container = document.getElementById('subject-list');
    container.innerHTML = '';
    
    if (!questionsData || !questionsData.subjects) {
        container.innerHTML = '<p class="no-data">문제 데이터가 없습니다.</p>';
        return;
    }
    
    questionsData.subjects.forEach(subject => {
        const item = document.createElement('div');
        item.className = 'menu-item subject-item';
        item.textContent = subject.name;
        item.onclick = () => selectSubject(subject);
        container.appendChild(item);
    });
}

// 과목 선택
function selectSubject(subject) {
    currentSubject = subject;
    navigationState = 'chapter';
    
    // 빵 부스러기 업데이트
    document.getElementById('crumb-subject').textContent = subject.name;
    document.getElementById('crumb-chapter').textContent = '';
    document.getElementById('crumb-section').textContent = '';
    
    // 메뉴 렌더링
    renderChapterList();
    
    // UI 업데이트
    document.getElementById('menu-level-chapter').querySelector('h3').textContent = subject.name;
    document.getElementById('menu-level-section').style.display = 'none';
    document.getElementById('menu-level-chapter').style.display = 'block';
    
    showControls();
}

// 분류1(챕터) 목록 렌더링
function renderChapterList() {
    const container = document.getElementById('chapter-list');
    container.innerHTML = '';
    
    if (!currentSubject || !currentSubject.chapters) return;
    
    currentSubject.chapters.forEach(chapter => {
        const item = document.createElement('div');
        item.className = 'menu-item chapter-item';
        item.innerHTML = `<strong>${chapter.name}</strong>`;
        item.onclick = () => selectChapter(chapter);
        container.appendChild(item);
    });
}

// 분류1(챕터) 선택
function selectChapter(chapter) {
    currentChapter = chapter;
    navigationState = 'section';
    
    // 빵 부스러기 업데이트
    document.getElementById('crumb-chapter').textContent = chapter.name;
    document.getElementById('crumb-section').textContent = '';
    
    // 섹션 목록 추출
    const sections = [...new Set(chapter.questions.map(q => q.section).filter(s => s))];
    
    if (sections.length === 0) {
        // 섹션이 없으면 바로 게임 유형 선택
        selectSection(null);
        return;
    }
    
    // 메뉴 렌더링
    renderSectionList(sections);
    
    // UI 업데이트
    document.getElementById('menu-level-chapter').style.display = 'none';
    document.getElementById('menu-level-section').style.display = 'block';
    document.getElementById('menu-level-section').querySelector('h3').textContent = chapter.name;
    
    showControls();
}

// 분류2(섹션) 목록 렌더링
function renderSectionList(sections) {
    const container = document.getElementById('section-list');
    container.innerHTML = '';
    
    // 전체 문제 수 표시
    const allItem = document.createElement('div');
    allItem.className = 'menu-item section-item all-item';
    allItem.innerHTML = `<strong>전체</strong> <span class="count">(${currentChapter.questions.length}문제)</span>`;
    allItem.onclick = () => selectSection(null);
    container.appendChild(allItem);
    
    sections.forEach(section => {
        const count = currentChapter.questions.filter(q => q.section === section).length;
        const item = document.createElement('div');
        item.className = 'menu-item section-item';
        item.innerHTML = `<strong>${section}</strong> <span class="count">(${count}문제)</span>`;
        item.onclick = () => selectSection(section);
        container.appendChild(item);
    });
}

// 분류2(섹션) 선택
function selectSection(section) {
    currentSection = section;
    navigationState = 'game';
    
    // 빵 부스러기 업데이트
    document.getElementById('crumb-section').textContent = section || '전체';
    
    // 문제 필터링
    if (section) {
        questions = currentChapter.questions.filter(q => q.section === section);
    } else {
        questions = [...currentChapter.questions];
    }
    
    // 메뉴 숨기고 게임 유형 선택 표시
    document.getElementById('menu-level-chapter').style.display = 'none';
    document.getElementById('menu-level-section').style.display = 'none';
    document.getElementById('game-type-selector').style.display = 'block';
    
    showControls();
}

// 게임 유형 선택
function selectGameType(type) {
    gameType = type;
    
    document.querySelectorAll('.type-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
}

// 게임 시작
function startGame() {
    let filteredQuestions = [...questions];
    
    if (gameType === 'type1') {
        filteredQuestions = questions.filter(q => q.type === 'type1');
    } else if (gameType === 'type2') {
        filteredQuestions = questions.filter(q => q.type === 'type2');
    }
    
    if (filteredQuestions.length === 0) {
        alert('선택한 유형의 문제가 없습니다.');
        return;
    }
    
    questions = filteredQuestions;
    currentQuestion = 0;
    score = 0;
    correctAnswers = 0;
    wrongAnswers = 0;
    
    document.getElementById('score').textContent = score;
    document.getElementById('total').textContent = questions.length;
    
    startTime = Date.now();
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(updateTimer, 1000);
    
    document.getElementById('game-type-selector').style.display = 'none';
    document.getElementById('game-area').style.display = 'flex';
    document.getElementById('stats').style.display = 'block';
    
    showQuestion();
}

// 타이머 업데이트
function updateTimer() {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const seconds = (elapsed % 60).toString().padStart(2, '0');
    document.getElementById('time').textContent = `${minutes}:${seconds}`;
}

// 진행률 업데이트
function updateProgress() {
    const progress = (currentQuestion / questions.length) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
}

// 문제 표시 (엑셀 순서대로)
function showQuestion() {
    if (currentQuestion >= questions.length) {
        showResult();
        return;
    }
    
    const q = questions[currentQuestion];
    const sentenceEl = document.getElementById('sentence');
    const hintEl = document.getElementById('hint');
    const inputsEl = document.getElementById('inputs');
    const messageEl = document.getElementById('message');
    
    document.getElementById('question-num').textContent = currentQuestion + 1;
    document.getElementById('question-num-display').textContent = `${currentQuestion + 1}번`;
    document.getElementById('question-type-display').textContent = q.type === 'type1' ? '선택형' : '빈칸형';
    
    if (q.type === 'type1') {
        // 선택형 문제
        sentenceEl.textContent = q.question;
        hintEl.textContent = '';
        
        inputsEl.innerHTML = '';
        inputsEl.style.display = 'flex';
        
        q.options.forEach((option, i) => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.textContent = `${i + 1}. ${option}`;
            btn.onclick = () => checkType1Answer(i + 1);
            inputsEl.appendChild(btn);
        });
        
        document.getElementById('submit-btn').style.display = 'none';
    } else {
        // 빈칸형 문제
        let displayQuestion = q.question;
        const blanks = displayQuestion.match(/<[^>]+>/g) || [];
        
        blanks.forEach((blank, i) => {
            displayQuestion = displayQuestion.replace(blank, `<span class="blank" data-index="${i}">(${i + 1})</span>`);
        });
        
        sentenceEl.innerHTML = displayQuestion;
        hintEl.textContent = `정답: ${q.answer}`;
        
        inputsEl.innerHTML = '';
        inputsEl.style.display = 'flex';
        
        const input = document.createElement('input');
        input.type = 'text';
        input.id = 'answer-0';
        input.placeholder = '정답 입력';
        input.setAttribute('aria-label', '정답 입력');
        inputsEl.appendChild(input);
        
        document.getElementById('submit-btn').style.display = 'inline-block';
    }
    
    messageEl.textContent = '';
    messageEl.className = 'message';
    
    document.getElementById('next-btn').style.display = 'none';
    
    const card = document.getElementById('question-card');
    card.style.animation = 'none';
    card.offsetHeight;
    card.style.animation = 'slideIn 0.3s ease';
    
    updateProgress();
    
    if (q.type === 'type2') {
        const firstInput = document.getElementById('answer-0');
        if (firstInput) firstInput.focus();
    }
}

// 선택형 답 확인
function checkType1Answer(selected) {
    const q = questions[currentQuestion];
    const isCorrect = selected === q.answer;
    
    const messageEl = document.getElementById('message');
    const buttons = document.querySelectorAll('.option-btn');
    
    buttons.forEach((btn, i) => {
        btn.disabled = true;
        if (i + 1 === q.answer) {
            btn.classList.add('correct');
        } else if (i + 1 === selected && !isCorrect) {
            btn.classList.add('wrong');
        }
    });
    
    if (isCorrect) {
        correctAnswers++;
        score += 10;
        messageEl.textContent = '정답입니다!';
        messageEl.className = 'message correct';
    } else {
        wrongAnswers++;
        messageEl.textContent = `틀렸습니다. 정답: ${q.answer}번`;
        messageEl.className = 'message wrong';
    }
    
    document.getElementById('score').textContent = score;
    document.getElementById('next-btn').style.display = 'inline-block';
    
    const scoreEl = document.getElementById('score');
    scoreEl.classList.add('animate');
    setTimeout(() => scoreEl.classList.remove('animate'), 500);
    
    updateAccuracy();
}

// 빈칸형 답 확인
function checkAnswer() {
    const q = questions[currentQuestion];
    const input = document.getElementById('answer-0');
    if (!input) return;
    
    const userAnswer = input.value.trim();
    const isCorrect = userAnswer === q.answer;
    
    const messageEl = document.getElementById('message');
    
    if (isCorrect) {
        correctAnswers++;
        score += 10;
        messageEl.textContent = '정답입니다!';
        messageEl.className = 'message correct';
        input.classList.add('correct');
        input.classList.remove('wrong');
        
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('next-btn').style.display = 'inline-block';
    } else {
        wrongAnswers++;
        messageEl.textContent = `틀렸습니다. 정답: ${q.answer}`;
        messageEl.className = 'message wrong';
        input.classList.add('wrong');
        input.classList.remove('correct');
        
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('next-btn').style.display = 'inline-block';
    }
    
    document.getElementById('score').textContent = score;
    updateAccuracy();
}

// 정확도 업데이트
function updateAccuracy() {
    const total = correctAnswers + wrongAnswers;
    const accuracy = total > 0 ? Math.round((correctAnswers / total) * 100) : 0;
    document.getElementById('accuracy').textContent = `${accuracy}%`;
}

// 다음 문제
function nextQuestion() {
    currentQuestion++;
    showQuestion();
}

// 결과 표시
function showResult() {
    if (timerInterval) clearInterval(timerInterval);
    
    const total = correctAnswers + wrongAnswers;
    const accuracy = total > 0 ? Math.round((correctAnswers / total) * 100) : 0;
    
    document.getElementById('final-score').textContent = score;
    document.getElementById('correct-count').textContent = correctAnswers;
    document.getElementById('wrong-count').textContent = wrongAnswers;
    document.getElementById('final-accuracy').textContent = `${accuracy}%`;
    
    document.getElementById('result-modal').style.display = 'flex';
}

// 다시 하기
function restartGame() {
    document.getElementById('result-modal').style.display = 'none';
    document.getElementById('game-area').style.display = 'none';
    document.getElementById('game-type-selector').style.display = 'block';
    document.getElementById('stats').style.display = 'none';
    document.getElementById('progress-bar').style.width = '0%';
}

// 뒤로 가기
function goBack() {
    if (navigationState === 'game') {
        navigationState = 'section';
        document.getElementById('game-area').style.display = 'none';
        document.getElementById('game-type-selector').style.display = 'none';
        document.getElementById('stats').style.display = 'none';
        
        if (currentSection) {
            document.getElementById('menu-level-section').style.display = 'block';
            document.getElementById('crumb-section').textContent = '';
        } else {
            document.getElementById('menu-level-chapter').style.display = 'block';
            document.getElementById('crumb-chapter').textContent = '';
        }
    } else if (navigationState === 'section') {
        navigationState = 'chapter';
        document.getElementById('menu-level-section').style.display = 'none';
        document.getElementById('menu-level-chapter').style.display = 'block';
        document.getElementById('crumb-chapter').textContent = '';
    } else if (navigationState === 'chapter') {
        navigationState = 'subject';
        document.getElementById('menu-level-chapter').style.display = 'none';
        document.getElementById('crumb-subject').textContent = '';
        hideControls();
    }
}

// 컨트롤 표시
function showControls() {
    document.getElementById('controls').style.display = 'block';
}

// 컨트롤 숨기기
function hideControls() {
    document.getElementById('controls').style.display = 'none';
}

// 사이드바 토글
document.getElementById('menu-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

// 키보드 단축키
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const submitBtn = document.getElementById('submit-btn');
        const nextBtn = document.getElementById('next-btn');
        
        if (submitBtn.style.display !== 'none') {
            checkAnswer();
        } else if (nextBtn.style.display !== 'none') {
            nextQuestion();
        }
    }
    
    if (e.key === 'Escape') {
        if (navigationState === 'game') {
            goBack();
        } else {
            document.getElementById('sidebar').classList.toggle('open');
        }
    }
    
    if (e.key === 'Backspace' && navigationState !== 'subject') {
        goBack();
    }
});

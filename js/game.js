// 상태 관리
let currentSubject = null;
let selectedChapter = null;
let selectedSection = null;
let gameType = 'all';
let allQuestions = [];
let questions = [];
let currentQuestion = 0;
let score = 0;
let correctAnswers = 0;
let wrongAnswers = 0;
let questionWrongCount = 0;
let startTime = null;
let timerInterval = null;

// 초기화
window.addEventListener('load', async () => {
    await loadQuestions();
    renderSubjectList();
    renderMenu();
    
    // 이벤트 리스너 등록
    document.querySelectorAll('.type-btn').forEach(btn => {
        btn.addEventListener('click', () => selectGameType(btn.dataset.type, btn));
    });
    
    document.getElementById('btn-start').addEventListener('click', startGame);
    document.getElementById('btn-back').addEventListener('click', backToMenu);
    document.getElementById('home-btn').addEventListener('click', backToMenu);
    document.getElementById('submit-btn').addEventListener('click', checkAnswer);
    document.getElementById('next-btn').addEventListener('click', nextQuestion);
    document.getElementById('btn-restart').addEventListener('click', restartGame);
    document.getElementById('menu-toggle').addEventListener('click', () => {
        document.getElementById('sidebar').classList.toggle('open');
    });
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
        item.addEventListener('click', () => selectSubject(subject, item));
        container.appendChild(item);
    });
}

// 과목 선택
function selectSubject(subject, element) {
    currentSubject = subject;
    document.getElementById('page-title').textContent = `📖 ${subject.name}`;
    
    // 사이드바 활성화 표시
    document.querySelectorAll('.subject-item').forEach(item => {
        item.classList.remove('active');
    });
    element.classList.add('active');
    
    renderMenu();
    document.getElementById('sidebar').classList.remove('open');
}

// 메뉴 렌더링 (한 페이지에 모든 챕터+섹션)
function renderMenu() {
    const container = document.getElementById('chapter-section');
    container.innerHTML = '';
    
    if (!currentSubject || !currentSubject.chapters) {
        container.innerHTML = '<p class="no-data">📚 과목을 선택해주세요</p>';
        return;
    }
    
    const chapterEmojis = ['📋', '📑'];
    
    currentSubject.chapters.forEach((chapter, chapterIdx) => {
        const chapterDiv = document.createElement('div');
        chapterDiv.className = 'chapter-block';
        
        const emoji = chapterEmojis[chapterIdx % chapterEmojis.length];
        
        const header = document.createElement('div');
        header.className = 'chapter-header';
        header.innerHTML = `<h3>${emoji} ${chapter.name}</h3>`;
        chapterDiv.appendChild(header);
        
        const sections = [...new Set(chapter.questions.map(q => q.section).filter(s => s))];
        
        const sectionList = document.createElement('div');
        sectionList.className = 'section-list';
        
        const allBtn = document.createElement('button');
        allBtn.className = 'section-btn all-btn';
        allBtn.innerHTML = `🎯 전체 <span class="count">(${chapter.questions.length})</span>`;
        allBtn.addEventListener('click', () => selectSection(chapter, null, allBtn));
        sectionList.appendChild(allBtn);
        
        sections.forEach(section => {
            const count = chapter.questions.filter(q => q.section === section).length;
            const btn = document.createElement('button');
            btn.className = 'section-btn';
            btn.innerHTML = `📌 ${section} <span class="count">(${count})</span>`;
            btn.addEventListener('click', () => selectSection(chapter, section, btn));
            sectionList.appendChild(btn);
        });
        
        chapterDiv.appendChild(sectionList);
        container.appendChild(chapterDiv);
    });
}

// 섹션 선택
function selectSection(chapter, section, btn) {
    selectedChapter = chapter;
    selectedSection = section;
    
    // 활성화 표시
    document.querySelectorAll('.section-btn').forEach(b => b.classList.remove('selected'));
    btn.classList.add('selected');
    
    // 문제 필터링
    if (section) {
        allQuestions = chapter.questions.filter(q => q.section === section);
    } else {
        allQuestions = [...chapter.questions];
    }
    questions = [...allQuestions];
    
    // 게임 유형 선택 표시
    document.getElementById('single-page-menu').style.display = 'none';
    document.getElementById('game-type-selector').style.display = 'block';
    
    // 선택 정보 표시
    const info = document.getElementById('selected-info');
    info.innerHTML = `📚 <strong>${chapter.name}</strong>${section ? ' > 📌 ' + section : ' > 🎯 전체'} - ${questions.length}문제`;
}

// 메뉴로 돌아가기
function backToMenu() {
    questions = [...allQuestions];
    document.getElementById('single-page-menu').style.display = 'block';
    document.getElementById('game-type-selector').style.display = 'none';
    document.getElementById('game-area').style.display = 'none';
    document.getElementById('stats').style.display = 'none';
    document.getElementById('progress-container').style.display = 'none';
    document.getElementById('progress-bar').style.width = '0%';
    document.getElementById('home-btn').style.display = 'none';
}

// 게임 유형 선택
function selectGameType(type, element) {
    gameType = type;
    document.querySelectorAll('.type-btn').forEach(btn => btn.classList.remove('selected'));
    element.classList.add('selected');
}

// 게임 시작
function startGame() {
    let gameQuestions = [...allQuestions];
    
    if (gameType === 'type1') {
        gameQuestions = allQuestions.filter(q => q.type === 'type1');
    } else if (gameType === 'type2') {
        gameQuestions = allQuestions.filter(q => q.type === 'type2');
    }
    
    if (gameQuestions.length === 0) {
        alert('선택한 유형의 문제가 없습니다.');
        return;
    }
    
    questions = gameQuestions;
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
    document.getElementById('single-page-menu').style.display = 'none';
    document.getElementById('game-area').style.display = 'flex';
    document.getElementById('stats').style.display = 'flex';
    document.getElementById('progress-container').style.display = 'block';
    document.getElementById('home-btn').style.display = 'inline-block';
    
    showQuestion();
}

// 타이머
function updateTimer() {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const seconds = (elapsed % 60).toString().padStart(2, '0');
    document.getElementById('time').textContent = `${minutes}:${seconds}`;
}

// 진행률
function updateProgress() {
    const progress = (currentQuestion / questions.length) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
}

// 빈칸 힌트 생성 함수 (글자→O, 공백→공백)
function getBlankHint(answer) {
    return answer.split('').map(char => {
        if (char === ' ') return ' ';
        return 'O';
    }).join('');
}

// 문제 표시
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
    
    questionWrongCount = 0;
    
    document.getElementById('question-num').textContent = currentQuestion + 1;
    document.getElementById('question-num-display').textContent = `${currentQuestion + 1}번`;
    document.getElementById('question-type-display').textContent = q.type === 'type1' ? '🔘 선택형' : '✏️ 빈칸형';
    
    if (q.type === 'type1') {
        sentenceEl.textContent = q.question;
        hintEl.textContent = '';
        inputsEl.innerHTML = '';
        inputsEl.style.display = 'flex';
        
        q.options.forEach((option, i) => {
            const btn = document.createElement('button');
            btn.className = 'option-btn';
            btn.textContent = `${i + 1}. ${option}`;
            btn.addEventListener('click', () => checkType1Answer(i + 1));
            inputsEl.appendChild(btn);
        });
        
        document.getElementById('submit-btn').style.display = 'none';
    } else {
        let displayQuestion = q.question;
        const blanks = displayQuestion.match(/<[^>]+>/g) || [];
        blanks.forEach((blank, i) => {
            displayQuestion = displayQuestion.replace(blank, `<span class="blank" data-index="${i}">(${i + 1})</span>`);
        });
        
        sentenceEl.innerHTML = displayQuestion;
        hintEl.textContent = blanks.length > 0 ? `${blanks.length}개의 빈칸을 채워주세요` : '';
        inputsEl.innerHTML = '';
        inputsEl.style.display = 'flex';
        
        const answerParts = q.answer.split('|');
        
        blanks.forEach((blank, i) => {
            const input = document.createElement('input');
            input.type = 'text';
            input.id = `answer-${i}`;
            const hint = getBlankHint(answerParts[i] || '');
            input.placeholder = `(${i + 1})번 답 입력: ${hint}`;
            inputsEl.appendChild(input);
        });
        
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
        if (i + 1 === q.answer) btn.classList.add('correct');
        else if (i + 1 === selected && !isCorrect) btn.classList.add('wrong');
    });
    
    if (isCorrect) {
        correctAnswers++;
        score += 10;
        messageEl.textContent = '🎉 정답입니다!';
        messageEl.className = 'message correct';
    } else {
        wrongAnswers++;
        messageEl.textContent = `😅 틀렸습니다. 정답은 ${q.answer}번이에요`;
        messageEl.className = 'message wrong';
    }
    
    document.getElementById('score').textContent = score;
    document.getElementById('next-btn').style.display = 'inline-block';
    updateAccuracy();
}

// 빈칸형 답 확인
function checkAnswer() {
    const q = questions[currentQuestion];
    const blanks = q.question.match(/<[^>]+>/g) || [];
    const messageEl = document.getElementById('message');
    const hintEl = document.getElementById('hint');
    
    const userAnswers = [];
    let allFilled = true;
    
    blanks.forEach((_, i) => {
        const input = document.getElementById(`answer-${i}`);
        if (input) {
            const val = input.value.trim();
            if (!val) allFilled = false;
            userAnswers.push(val);
        }
    });
    
    if (!allFilled) {
        messageEl.textContent = '모든 빈칸을 입력해주세요!';
        messageEl.className = 'message wrong';
        return;
    }
    
    const correctAnsArr = q.answer.split('|').map(a => a.trim());
    let allCorrect = true;
    
    blanks.forEach((_, i) => {
        const input = document.getElementById(`answer-${i}`);
        const userAns = userAnswers[i];
        const correctAns = correctAnsArr[i];
        
        if (userAns === correctAns) {
            input.classList.add('correct');
            input.disabled = true;
        } else {
            input.classList.add('wrong');
            allCorrect = false;
        }
    });
    
    if (allCorrect) {
        correctAnswers++;
        score += 10;
        messageEl.textContent = '🎉 정답입니다!';
        messageEl.className = 'message correct';
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('next-btn').style.display = 'inline-block';
    } else {
        questionWrongCount++;
        wrongAnswers++;
        
        blanks.forEach((_, i) => {
            const input = document.getElementById(`answer-${i}`);
            if (!input.classList.contains('correct')) {
                input.value = '';
                input.classList.remove('wrong');
                input.disabled = false;
                input.focus();
            }
        });
        
        if (questionWrongCount >= 3) {
            let ansText = correctAnsArr.join(', ');
            messageEl.textContent = `😅 3번 틀렸습니다. 정답은 "${ansText}"이에요`;
            messageEl.className = 'message wrong';
            hintEl.textContent = `💡 다음 문제에서 더 잘할 수 있어요!`;
            blanks.forEach((_, i) => {
                const input = document.getElementById(`answer-${i}`);
                input.disabled = true;
            });
            document.getElementById('submit-btn').style.display = 'none';
            document.getElementById('next-btn').style.display = 'inline-block';
        } else {
            messageEl.textContent = `😅 틀렸습니다. (${questionWrongCount}/3) 다시 시도해보세요!`;
            messageEl.className = 'message wrong';
        }
    }
    
    document.getElementById('score').textContent = score;
    updateAccuracy();
}

// 정확도
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

// 결과
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
    document.getElementById('stats').style.display = 'none';
    backToMenu();
}

// 키보드
document.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        const submitBtn = document.getElementById('submit-btn');
        const nextBtn = document.getElementById('next-btn');
        if (submitBtn.style.display !== 'none') checkAnswer();
        else if (nextBtn.style.display !== 'none') nextQuestion();
    }
    if (e.key === 'Escape') {
        if (document.getElementById('game-area').style.display !== 'none') {
            backToMenu();
        } else {
            document.getElementById('sidebar').classList.toggle('open');
        }
    }
});

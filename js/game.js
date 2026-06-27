let currentTopic = 'civil';
let gameType = 'blank';
let questions = [];
let currentQuestion = 0;
let score = 0;
let attemptCount = 0;
let correctAnswers = 0;
let wrongAnswers = 0;
let startTime = null;
let timerInterval = null;

function shuffleArray(array) {
    const shuffled = [...array];
    for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled;
}

function selectTopic(topic) {
    currentTopic = topic;
    
    document.querySelectorAll('.topic-item').forEach(item => {
        item.classList.remove('active');
    });
    document.querySelector(`[data-topic="${topic}"]`).classList.add('active');
    
    if (questionsData && questionsData[topic]) {
        document.getElementById('topic-title').textContent = questionsData[topic].title;
    }
    score = 0;
    document.getElementById('score').textContent = score;
    
    document.getElementById('sidebar').classList.remove('open');
}

function selectGameType(type) {
    gameType = type;
    
    document.querySelectorAll('.type-btn').forEach(btn => {
        btn.classList.remove('selected');
    });
    event.currentTarget.classList.add('selected');
}

function startGame() {
    if (!questionsData) {
        alert('문제가 로딩되지 않았습니다. 페이지를 새로고침해주세요.');
        return;
    }
    
    const data = questionsData[currentTopic];
    
    if (gameType === 'ox') {
        if (!data.ox || data.ox.length === 0) {
            alert('OX 문제가 없습니다.');
            return;
        }
        questions = shuffleArray(data.ox).slice(0, 5);
    } else {
        if (!data.blank || data.blank.length === 0) {
            alert('빈칸 문제가 없습니다.');
            return;
        }
        questions = shuffleArray(data.blank).slice(0, 5);
    }
    
    currentQuestion = 0;
    score = 0;
    correctAnswers = 0;
    wrongAnswers = 0;
    attemptCount = 0;
    
    document.getElementById('score').textContent = score;
    document.getElementById('total').textContent = questions.length;
    
    startTime = Date.now();
    if (timerInterval) clearInterval(timerInterval);
    timerInterval = setInterval(updateTimer, 1000);
    
    document.getElementById('game-type-selector').style.display = 'none';
    document.getElementById('game-area').style.display = 'flex';
    document.getElementById('controls').style.display = 'none';
    document.getElementById('stats').style.display = 'block';
    
    showQuestion();
}

function updateTimer() {
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const minutes = Math.floor(elapsed / 60).toString().padStart(2, '0');
    const seconds = (elapsed % 60).toString().padStart(2, '0');
    document.getElementById('time').textContent = `${minutes}:${seconds}`;
}

function updateProgress() {
    const progress = (currentQuestion / questions.length) * 100;
    document.getElementById('progress-bar').style.width = `${progress}%`;
}

function showQuestion() {
    if (currentQuestion >= questions.length) {
        showResult();
        return;
    }
    
    const q = questions[currentQuestion];
    const titleEl = document.getElementById('question-title');
    const sentenceEl = document.getElementById('sentence');
    const hintEl = document.getElementById('hint');
    const oxButtonsEl = document.getElementById('ox-buttons');
    const inputsEl = document.getElementById('inputs');
    const messageEl = document.getElementById('message');
    
    attemptCount = 0;
    document.getElementById('question-num').textContent = currentQuestion + 1;
    
    if (gameType === 'ox') {
        titleEl.textContent = '';
        sentenceEl.textContent = q.statement;
        hintEl.textContent = `힌트: ${q.hint}`;
        oxButtonsEl.style.display = 'flex';
        inputsEl.style.display = 'none';
        document.getElementById('submit-btn').style.display = 'none';
    } else {
        titleEl.textContent = q.title || '';
        let sentenceHtml = q.paragraph || q.template;
        const blankCount = (sentenceHtml.match(/__/g) || []).length;
        for (let i = 0; i < blankCount; i++) {
            sentenceHtml = sentenceHtml.replace('__', `<span class="blank" data-index="${i}">(${i + 1})</span>`);
        }
        sentenceEl.innerHTML = sentenceHtml;
        hintEl.textContent = `힌트: ${q.hint}`;
        oxButtonsEl.style.display = 'none';
        inputsEl.style.display = 'flex';
        inputsEl.innerHTML = '';
        q.blanks.forEach((_, i) => {
            const input = document.createElement('input');
            input.type = 'text';
            input.id = `answer-${i}`;
            input.placeholder = `${i + 1}번 답`;
            input.setAttribute('aria-label', `${i + 1}번 답 입력`);
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
    
    if (gameType === 'blank') {
        const firstInput = document.getElementById('answer-0');
        if (firstInput) firstInput.focus();
    }
}

function checkOX(userAnswer) {
    const q = questions[currentQuestion];
    const isCorrect = userAnswer === q.answer;
    
    const messageEl = document.getElementById('message');
    if (isCorrect) {
        correctAnswers++;
        score += 10;
        messageEl.textContent = '정답입니다!';
        messageEl.className = 'message correct';
    } else {
        wrongAnswers++;
        messageEl.textContent = `틀렸습니다. 정답: ${q.answer ? 'O' : 'X'}`;
        messageEl.className = 'message wrong';
    }
    
    document.getElementById('score').textContent = score;
    document.getElementById('ox-buttons').style.display = 'none';
    document.getElementById('next-btn').style.display = 'inline-block';
    
    const scoreEl = document.getElementById('score');
    scoreEl.classList.add('animate');
    setTimeout(() => scoreEl.classList.remove('animate'), 500);
    
    updateAccuracy();
}

function checkAnswer() {
    const q = questions[currentQuestion];
    let correctCount = 0;
    
    q.blanks.forEach((correctAnswer, i) => {
        const input = document.getElementById(`answer-${i}`);
        if (!input) return;
        
        const userAnswer = input.value.trim();
        const blankEl = document.querySelector(`.blank[data-index="${i}"]`);
        
        if (userAnswer === correctAnswer) {
            correctCount++;
            input.classList.add('correct');
            input.classList.remove('wrong');
            if (blankEl) {
                blankEl.style.color = '#10b981';
                blankEl.textContent = correctAnswer;
            }
        } else {
            input.classList.add('wrong');
            input.classList.remove('correct');
            if (blankEl) {
                blankEl.style.color = '#ef4444';
            }
        }
    });
    
    const messageEl = document.getElementById('message');
    if (correctCount === q.blanks.length) {
        correctAnswers++;
        score += 10;
        messageEl.textContent = '정답입니다!';
        messageEl.className = 'message correct';
        document.getElementById('submit-btn').style.display = 'none';
        document.getElementById('next-btn').style.display = 'inline-block';
        
        const scoreEl = document.getElementById('score');
        scoreEl.classList.add('animate');
        setTimeout(() => scoreEl.classList.remove('animate'), 500);
    } else {
        attemptCount++;
        if (attemptCount >= 5) {
            wrongAnswers++;
            const correctText = q.blanks.join(', ');
            messageEl.textContent = `5번 틀렸습니다. 정답: ${correctText}`;
            messageEl.className = 'message wrong';
            document.getElementById('submit-btn').style.display = 'none';
            document.getElementById('next-btn').style.display = 'inline-block';
            
            q.blanks.forEach((correctAnswer, i) => {
                const blankEl = document.querySelector(`.blank[data-index="${i}"]`);
                if (blankEl) {
                    blankEl.style.color = '#10b981';
                    blankEl.textContent = correctAnswer;
                }
            });
        } else {
            messageEl.textContent = `틀렸습니다. (${attemptCount}/5)`;
            messageEl.className = 'message wrong';
        }
    }
    
    document.getElementById('score').textContent = score;
    updateAccuracy();
}

function updateAccuracy() {
    const total = correctAnswers + wrongAnswers;
    const accuracy = total > 0 ? Math.round((correctAnswers / total) * 100) : 0;
    document.getElementById('accuracy').textContent = `${accuracy}%`;
}

function nextQuestion() {
    currentQuestion++;
    showQuestion();
}

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

function restartGame() {
    document.getElementById('result-modal').style.display = 'none';
    document.getElementById('game-type-selector').style.display = 'block';
    document.getElementById('game-area').style.display = 'none';
    document.getElementById('controls').style.display = 'block';
    document.getElementById('stats').style.display = 'none';
    document.getElementById('progress-bar').style.width = '0%';
}

document.getElementById('menu-toggle').addEventListener('click', () => {
    document.getElementById('sidebar').classList.toggle('open');
});

document.querySelectorAll('.topic-item').forEach(item => {
    item.addEventListener('click', () => {
        selectTopic(item.dataset.topic);
    });
});

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
        document.getElementById('sidebar').classList.toggle('open');
    }
});

window.addEventListener('load', async () => {
    await loadQuestions();
    selectTopic('civil');
});

document.addEventListener("DOMContentLoaded", function () {
    fetchQuestion();

    // Enter 키를 눌렀을 때 정답 제출 또는 다음 문제로 이동
    document.getElementById("user-answer").addEventListener("keydown", function (event) {
        if (event.key === "Enter") {
            if (document.getElementById("result-box").style.display === "block") {
                nextQuestion();
            } else {
                submitAnswer();
            }
        }
    });
});

function fetchQuestion() {
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            if (data.end) {
                // 10문제 종료 시 점수 표시
                displayScore(data.correct_count);
            } else {
                // 문제 표시 및 기존 정답 입력값 초기화
                document.getElementById("question-title").textContent = data.question.split("\n")[0];
                document.getElementById("question-text").innerHTML = data.question.split("\n").slice(1).join("<br>").replace("□", '<span class="question-mark-box">?</span>');
                document.querySelector(".answer-box").classList.remove("hidden");
                document.querySelector(".submit-button").classList.remove("hidden");
                document.getElementById("user-answer").value = "";  // 이전 입력값 제거
            }
        });
}

function submitAnswer() {
    const userAnswer = document.getElementById("user-answer").value;
    const correctAnswer = document.getElementById("question-title").textContent;

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: userAnswer, correct_answer: correctAnswer })
    })
    .then(response => response.json())
    .then(data => {
        const resultBox = document.getElementById("result-box");
        const resultMessage = document.getElementById("result-message");

        if (data.result) {
            resultMessage.innerHTML = `<span style="font-weight: normal;">정답!</span><br><span style="display: inline-block; margin-top: 10px;">${data.correct_answer}</span>`;
        } else {
            resultMessage.innerHTML = `<span style="font-weight: normal;">오답!</span><br><span style="display: inline-block; margin-top: 10px;">${data.correct_answer}</span>`;
        }
        resultBox.style.display = "block";  // 결과 박스 표시
        document.querySelector(".answer-box").classList.add("hidden");  // 입력창 숨김
        document.querySelector(".submit-button").classList.add("hidden");  // 제출 버튼 숨김
    });
}

function nextQuestion() {
    document.getElementById("result-box").style.display = "none";  // 결과 박스 숨김
    fetchQuestion();  // 새로운 문제 요청
}

function displayScore(correctCount) {
    // 10문제 후 정답 수 결과 표시
    const resultBox = document.getElementById("result-box");
    const resultMessage = document.getElementById("result-message");

    resultMessage.innerHTML = `게임 종료!<br>총 10문제 중 ${correctCount}문제를 맞췄습니다.`;
    document.querySelector(".next-button").style.display = "none";  // 다음 버튼 숨김
    document.getElementById("user-answer").disabled = true;  // 정답 입력창 비활성화
}

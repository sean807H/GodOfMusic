document.addEventListener("DOMContentLoaded", function () {
    fetchQuestion();
});

function fetchQuestion() {
    fetch('/get_question')
        .then(response => response.json())
        .then(data => {
            document.getElementById("question-title").textContent = data.question.split("\n")[0];
            document.getElementById("question-text").innerHTML = data.question.split("\n").slice(1).join("<br>").replace("□", '<span class="question-mark-box">?</span>');
            document.querySelector(".answer-box").classList.remove("hidden");
            document.querySelector(".submit-button").classList.remove("hidden");
            // 정답 확인을 위한 현재 질문에 대한 정답 저장
            document.getElementById("correct-answer").value = data.answer;
        });
}

function submitAnswer() {
    const userAnswer = document.getElementById("user-answer").value;
    const correctAnswer = document.getElementById("correct-answer").value;

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: userAnswer, correct_answer: document.getElementById("question-title").textContent })
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
        
        resultBox.style.display = "block";
        document.querySelector(".answer-box").classList.add("hidden");
        document.querySelector(".submit-button").classList.add("hidden");
    });
}

function nextQuestion() {
    document.getElementById("user-answer").value = "";
    document.getElementById("result-box").style.display = "none";
    fetchQuestion();
}

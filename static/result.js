document.addEventListener("DOMContentLoaded", function () {
    fetch('/get_result')
        .then(response => response.json())
        .then(data => {
            document.getElementById("correct-count").textContent = data.correct_count;
            document.getElementById("wrong-count").textContent = 10 - data.correct_count;
        });
});

function restartQuiz() {
    window.location.href = '/';  // 퀴즈 재시작
}

function goToAnotherQuiz() {
    window.location.href = '/another_quiz';  // 다른 퀴즈 페이지로 이동 (기능에 따라 추가 가능)
}

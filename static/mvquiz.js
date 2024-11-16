function submitAnswer() {
    const userAnswer = document.getElementById("answer-input").value;

    fetch('/check_answer', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer: userAnswer })
    })
    .then(response => response.json())
    .then(data => {
        // 입력 박스와 버튼 숨기기
        document.querySelector(".answer-box").style.display = "none";
        document.querySelector(".submit-button").style.display = "none";
        document.getElementById("scene-image").style.display = "none";

        // 정답 화면 표시
        const resultContainer = document.getElementById("result-container");
        resultContainer.classList.remove("hidden");
        document.getElementById("result-text").innerText = data.result ? "정답!" : "오답!";
        document.getElementById("song-title").innerText = data.songTitle;

        const resultImage = document.getElementById("result-image");
        resultImage.src = data.correctImage;

        // 화살표 버튼에 마지막 문제 여부 저장
        const nextButton = document.querySelector("button[onclick='nextQuestion()']");
        nextButton.dataset.endQuiz = data.endQuiz; // 마지막 문제인지 여부 저장
    })
    .catch(error => console.error("Error:", error));
}

function nextQuestion() {
    const nextButton = document.querySelector("button[onclick='nextQuestion()']");
    const isEndQuiz = nextButton.dataset.endQuiz === "true";

    if (isEndQuiz) {
        // 마지막 문제라면 결과 페이지로 이동
        window.location.href = '/result';
    } else {
        // 다음 문제로 이동
        fetch('/load_next_question')
        .then(response => response.json())
        .then(data => {
            // 다음 문제의 이미지와 입력란 표시
            const sceneImage = document.getElementById("scene-image");
            sceneImage.src = data.image;
            sceneImage.style.display = "block";
            sceneImage.style.width = "884px";
            sceneImage.style.height = "423px";

            // 입력창과 버튼 스타일 초기화
            document.getElementById("answer-input").value = "";
            document.querySelector(".answer-box").style.display = "flex";
            document.querySelector(".answer-box").style.justifyContent = "center";
            document.querySelector(".submit-button").style.display = "inline-block";

            // 결과 화면 숨기기
            const resultContainer = document.getElementById("result-container");
            resultContainer.classList.add("hidden");
        })
        .catch(error => console.error("Error:", error));
    }
}



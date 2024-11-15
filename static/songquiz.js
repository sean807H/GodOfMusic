// HTML에서 오디오 파일 경로 가져오기
const audioFilePath = document.querySelector(".container").getAttribute("data-audio");
let audio = new Audio(audioFilePath); // HTML에서 가져온 오디오 파일 경로 사용
let isPlaying = false;
let playTimeout;

function playAudio() {
    const soundIcon = document.getElementById("sound-icon");

    if (isPlaying) {
        // 오디오가 재생 중이면 멈춤
        audio.pause();
        isPlaying = false;
        soundIcon.classList.replace("bi-volume-mute-fill", "bi-volume-up-fill");
    } else {
        // 오디오가 재생 중이 아니면 재생
        if (audio.currentTime === 0 || audio.ended) {
            audio.currentTime = 0; // 처음부터 재생
        }
        audio.play();
        isPlaying = true;
        soundIcon.classList.replace("bi-volume-up-fill", "bi-volume-mute-fill");

        // 30초 후 자동으로 멈춤
        playTimeout = setTimeout(() => {
            audio.pause();
            audio.currentTime = 0; // 자동 멈춤 후 다시 처음으로
            isPlaying = false;
            soundIcon.classList.replace("bi-volume-mute-fill", "bi-volume-up-fill");
        }, 30000);
    }
}

// 오디오가 종료되었을 때 상태를 초기화
audio.onended = function () {
    isPlaying = false;
    document.getElementById("sound-icon").classList.replace("bi-volume-mute-fill", "bi-volume-up-fill");
};

function submitAnswer() {
    const userAnswer = document.getElementById("answer-input").value;

    fetch('/check_answer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ answer: userAnswer })
    })
        .then(response => response.json())
        .then(data => {
            // 정답 확인 및 화면 업데이트
            if (data.result) {
                document.getElementById("result-text").innerText = "정답!";
            } else {
                document.getElementById("result-text").innerText = "오답!";
            }

            // 여기에서 유튜브 iframe 스타일 조정
            const videoIframe = document.getElementById("music-video");
            videoIframe.style.width = "800px";
            videoIframe.style.height = "400px";
            videoIframe.style.marginBottom = "30px";

            document.getElementById("song-title").innerText = data.songTitle;
            document.getElementById("music-video").src = data.videoUrl;
            document.getElementById("result-container").classList.remove("hidden");

            // 요소들 숨기기
            document.querySelector(".sound-icon").style.display = "none";
            document.querySelector(".answer-box input[type='text']").style.display = "none";
            document.querySelector(".submit-button").style.display = "none";

            // 정답 화면으로 넘어갈 때 오디오 멈추기
            audio.pause();
            audio.currentTime = 0;
            isPlaying = false;
            document.getElementById("sound-icon").classList.replace("bi-volume-mute-fill", "bi-volume-up-fill");

            // endQuiz 플래그를 설정하여 다음 문제 클릭 시 결과 페이지로 이동하도록 설정
            if (data.endQuiz) {
                sessionStorage.setItem("endQuiz", "true"); // sessionStorage에 endQuiz 플래그 설정
            }
        })
        .catch(error => console.error("Error:", error));
}


function nextQuestion() {
    // 마지막 문제인 경우 결과 페이지로 이동
    if (sessionStorage.getItem("endQuiz") === "true") {
        window.location.href = '/result';
        sessionStorage.removeItem("endQuiz"); // 플래그 초기화
        return;
    }

    // 다음 문제 요청을 통해 새 문제 로드
    fetch('/quiz')
        .then(response => response.json())
        .then(data => {
            // 새 오디오 파일 경로 설정
            audio = new Audio(data.audio_file);
            isPlaying = false;

            // UI 요소 초기화
            document.getElementById("sound-icon").style.display = "inline-block";
            document.getElementById("result-container").classList.add("hidden");
            document.querySelector(".answer-box input[type='text']").style.display = "inline-block";
            document.querySelector(".submit-button").style.display = "inline-block";
            document.getElementById("answer-input").value = "";  // 입력 필드 초기화

            // 아이콘 초기화
            document.getElementById("sound-icon").classList.replace("bi-volume-mute-fill", "bi-volume-up-fill");
        })
        .catch(error => console.error("Error:", error));
}

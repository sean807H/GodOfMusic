function navigateToQuiz(quizType) {
    let url = '';
    
    switch (quizType) {
        case 'lyrics':
            url = "/game"; // /game으로 이동 (가사 맞추기)
            break;
        case 'title':
            url = "/explain"; // /explain으로 이동 (노래 제목 맞추기)
            break;
        case 'karaoke':
            url = "/songquiz"; // /songquiz으로 이동 (노래 듣고 맞추기)
            break;
        case 'music_video':
            url = "/mvquiz"; // /mvquiz으로 이동 (뮤직비디오 맞추기)
            break;
        default:
            console.error("Invalid quiz type");
            return;
    }

    // 선택한 경로로 이동
    window.location.href = url;
}
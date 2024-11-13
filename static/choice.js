function navigateToQuiz(quizType) {
    let url = '';
    
    switch (quizType) {
        case 'lyrics':
            url = "/game"; // /game으로 이동
            break;
        case 'title':
            url = "/explain"; // /title_quiz로 이동
            break;
        case 'karaoke':
            url = "/karaoke_quiz"; // /karaoke_quiz로 이동
            break;
        case 'music_video':
            url = "/music_video_quiz"; // /music_video_quiz로 이동
            break;
        default:
            console.error("Invalid quiz type");
            return;
    }

    // 선택한 경로로 이동
    window.location.href = url;
}

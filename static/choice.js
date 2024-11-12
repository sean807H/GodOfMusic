// 각 퀴즈 경로를 설정합니다.
function navigateToQuiz(quizType) {
    let url = '';
    
    switch (quizType) {
        case 'lyrics':
            url = "{{ url_for('lyrics_quiz') }}";
            break;
        case 'title':
            url = "{{ url_for('title_quiz') }}";
            break;
        case 'karaoke':
            url = "{{ url_for('karaoke_quiz') }}";
            break;
        case 'music_video':
            url = "{{ url_for('music_video_quiz') }}";
            break;
        default:
            console.error("Invalid quiz type");
            return;
    }

    // 선택한 경로로 이동
    window.location.href = url;
}



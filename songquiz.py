from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)  # 비밀 키 설정

# 10개의 노래 데이터
songquiz_data = [
    {"audio": "/static/audio/손오공.mp3", "answer": "손오공", "music_video_url": "https://www.youtube.com/embed/-GQg25oP0S4"},
    {"audio": "/static/audio/Dunk Shot.mp3", "answer": "Dunk shot,덩크슛", "music_video_url": "https://www.youtube.com/embed/4vgac97VlCE"},
    {"audio": "/static/audio/Songbird.mp3", "answer": "Songbird,송버드", "music_video_url": "https://www.youtube.com/embed/2XqVNFBtVo4"},
    {"audio": "/static/audio/WISH.mp3", "answer": "Wish,위시", "music_video_url": "https://www.youtube.com/embed/hvQZs3k6Ytk"},
    {"audio": "/static/audio/Siren.mp3", "answer": "Siren,사이렌", "music_video_url": "https://www.youtube.com/embed/UOPcXDvGmRs"},
    {"audio": "/static/audio/부모님관람불가.mp3", "answer": "부모님관람불가", "music_video_url": "https://www.youtube.com/embed/YkCXVgcsGTU"},
    {"audio": "/static/audio/박수.mp3", "answer": "박수", "music_video_url": "https://www.youtube.com/embed/CyzEtbG-sxY"},
    {"audio": "/static/audio/Darl+ing.mp3", "answer": "Darl+ing, 달링", "music_video_url": "https://www.youtube.com/embed/bTtNV6hgDno"},
    {"audio": "/static/audio/Happy.mp3", "answer": "Happy,해피", "music_video_url": "https://www.youtube.com/embed/sWXGbkM0tBI"},
    {"audio": "/static/audio/Whiplash.mp3", "answer": "Whiplash,위플래쉬,위플래시", "music_video_url": "https://www.youtube.com/embed/jWQx2f-CErU"}
]

@app.route('/')
def home():
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['seen_questions'] = []
    current_song = get_new_question() 
    session["current_song"] = current_song  
    return render_template('songquiz.html', audio_file=current_song["audio"])

def get_new_question():
    seen_questions = session.get("seen_questions", [])
    remaining_questions = [q for q in songquiz_data if q["audio"] not in seen_questions]

    if not remaining_questions:
        session['seen_questions'] = []
        remaining_questions = songquiz_data[:]

    question = random.choice(remaining_questions)
    seen_questions.append(question["audio"])
    session["seen_questions"] = seen_questions
    
    return question


@app.route('/quiz')
def quiz():
    if session['answered_count'] >= 10:
        return jsonify({"endQuiz": True})  # 마지막 문제일 경우 endQuiz 플래그 설정
    
    question = get_new_question()
    session["current_answer"] = question["answer"].split(',')[0]  # 중복 제거를 위해 첫 번째 정답만 사용
    session["current_song"] = question
    return jsonify({
        "audio_file": question["audio"],
        "question_text": "새로운 문제입니다",  # 필요한 경우 여기에 실제 질문 텍스트를 추가
        "endQuiz": False  # 마지막 문제가 아닐 경우
    })


@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get("answer").strip().lower()
    correct_answers = [ans.strip().lower() for ans in session["current_song"]["answer"].split(',')]
    
    is_correct = user_answer in correct_answers
    session['answered_count'] += 1
    if is_correct:
        session['correct_count'] += 1

    response = {
        "result": is_correct,
        "correct_answer": correct_answers[0],
        "videoUrl": session["current_song"]["music_video_url"],
        "songTitle": correct_answers[0]
    }

    # 마지막 문제 후 결과 화면으로 이동 설정
    if session['answered_count'] >= 10:
        response["endQuiz"] = True
    else:
        response["endQuiz"] = False
    
    return jsonify(response)

@app.route('/result')
def result():
    correct_count = session.get('correct_count', 0)
    incorrect_count = 10 - correct_count
    quiz_type = session.get('quiz_type', 'karaoke')  # 기본적으로 'karaoke'로 설정
    return render_template('result.html', correct_count=correct_count, incorrect_count=incorrect_count, quiz_type=quiz_type)

@app.route('/restart_quiz/<quiz_type>')
def restart_quiz(quiz_type):
    # 세션 초기화 후 선택된 퀴즈 타입의 첫 화면으로 이동
    session.clear()
    if quiz_type == 'karaoke':
        return redirect(url_for('home'))  # songquiz 첫 화면
    else:
        return redirect("http://localhost:5000/")  # 다른 퀴즈 페이지(app.py)로 이동

@app.route('/another_quiz')
def another_quiz():
    return redirect("http://localhost:5000/")  # 다른 퀴즈로 이동

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

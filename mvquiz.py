from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)

# 퀴즈 데이터
mvquiz_data = [
    {"image": "/static/images/apt.png", "answer": "apt, 아파트"},
    {"image": "/static/images/사랑돈명예.png", "answer": "사랑 돈 명예, love money fame"},
    {"image": "/static/images/boomboombase.png", "answer": "boomboombase, 붐붐베이스"},
    {"image": "/static/images/steady.png", "answer": "steady, 스테디"},
    {"image": "/static/images/supersonic.png", "answer": "supersonic, 수퍼소닉"},
    {"image": "/static/images/xo.png", "answer": "xo"},
    {"image": "/static/images/mantra.png", "answer": "mantra, 만트라"},
    {"image": "/static/images/power.png", "answer": "power, 파워"},
    {"image": "/static/images/serenade.png", "answer": "serenade, 세레나데"},
    {"image": "/static/images/네모네모.png", "answer": "네모네모"}
]

@app.route('/')
def quiz():
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['used_questions'] = []
    return redirect(url_for('next_question'))

@app.route('/next_question')
def next_question():
    if session['answered_count'] >= 10:
        return redirect(url_for('results'))

    available_questions = [q for q in mvquiz_data if q['image'] not in session['used_questions']]
    if not available_questions:
        session['used_questions'] = []
        available_questions = mvquiz_data[:]

    question = random.choice(available_questions)
    session['used_questions'].append(question['image'])
    session['current_question'] = question
    return render_template('mvquiz.html', scene=question)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    user_answer = request.json.get('answer').strip().lower()
    correct_answers = session['current_question']['answer'].lower().split(',')

    is_correct = user_answer in [answer.strip() for answer in correct_answers]
    session['answered_count'] += 1
    if is_correct:
        session['correct_count'] += 1


    # 마지막 문제인 경우 endQuiz를 True로 설정하지만, 정답 화면을 먼저 보여줌
    is_last_question = session['answered_count'] >= 10

    return jsonify({
        'result': is_correct,
        'songTitle': correct_answers[0],  # 첫 번째 답만 표시
        'correctImage': session['current_question']['image'],
        'endQuiz': is_last_question  # 마지막 문제 여부
    })

@app.route('/load_next_question')
def load_next_question():
    if session['answered_count'] >= 10:
        return redirect(url_for('results'))

    # Filter available questions and pick randomly
    available_questions = [q for q in mvquiz_data if q['image'] not in session['used_questions']]
    if not available_questions:
        session['used_questions'] = []
        available_questions = mvquiz_data[:]

    question = random.choice(available_questions)
    session['used_questions'].append(question['image'])
    session['current_question'] = question

    return jsonify({
        'image': question['image']
    })


@app.route('/result')
def result():
    correct_count = session.get('correct_count', 0)
    incorrect_count = 10 - correct_count
    quiz_type = session.get('quiz_type', 'music_video')  # 기본적으로 'karaoke'로 설정
    return render_template('result.html', correct_count=correct_count, incorrect_count=incorrect_count, quiz_type=quiz_type)

@app.route('/restart_quiz/<quiz_type>')
def restart_quiz(quiz_type):
    # 세션 초기화 후 선택된 퀴즈 타입의 첫 화면으로 이동
    session.clear()
    if quiz_type == 'music_video':
        return redirect(url_for('quiz'))  # mvquiz 첫 화면으로 이동
    else:
        return redirect("http://localhost:5000/")  # 다른 퀴즈 페이지(app.py)로 이동

@app.route('/another_quiz')
def another_quiz():
    return redirect("http://localhost:5000/")  # 다른 퀴즈로 이동


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# 예시 문제 리스트
questions = [
    # 문제 리스트 작성
]

@app.route('/')
def index():
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['question_pool'] = random.sample(questions, len(questions))
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    if session['answered_count'] >= 10:
        return redirect(url_for('result'))
    
    question = session['question_pool'].pop()
    session['current_answer'] = question['answer']
    return jsonify({"question": question['question'], "end": False})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get("answer", "").strip()
    correct_answer = session['current_answer']

    is_correct = user_answer.lower() == correct_answer.lower()
    session['answered_count'] += 1

    if is_correct:
        session['correct_count'] += 1

    return jsonify({"result": is_correct, "correct_answer": correct_answer})

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/get_result', methods=['GET'])
def get_result():
    correct_count = session.get('correct_count', 0)
    return jsonify({"correct_count": correct_count})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

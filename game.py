from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# 예시 문제 리스트
questions = [
    {"question": "DAY6 <Happy>\n그런 날이 있을까요?\n□을 찾게 되는 날이요", "answer": "꿈"},
    {"question": "DAY6 <예뻤어>\n사랑한다고 해줘\n□게 웃던 날", "answer": "고맙"},
    # 여기에 추가 문제를 작성하세요
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    question = random.choice(questions)
    return jsonify(question)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get("answer", "").strip()
    correct_answer = data.get("correct_answer", "")
    # questions에서 정답을 찾아 반환
    actual_answer = next((q["answer"] for q in questions if q["question"].startswith(correct_answer)), "")
    return jsonify({"result": user_answer.lower() == actual_answer.lower(), "correct_answer": actual_answer})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

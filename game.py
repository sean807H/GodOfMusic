from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random

def lyrics_quiz():
    return render_template('lyrics_quiz.html')

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 비밀 키 설정

# 예시 문제 리스트
questions = [
    {"question": "DAY6 <Happy>\n그런 날이 있을까요?\n□을 찾게 되는 날이요", "answer": "꿈"},    
    {"question": "QWER <내 이름 맑음>\n어쩌다 고작 그 □도 못 참고\n멍청하게 다 던졌는지", "answer": "마음"},
    {"question": "에스파 <Supernova>\nCan’t stop hyperstellar\n□그걸 찾아", "answer": "원초"},
    {"question": "이클립스 <소나기>\n그대는 □입니다\n하늘이 내려준", "answer": "선물"},
    {"question": "(여자)아이들 <클락션>\n힙합보다 멋진 발라드틱 Romantic show\n너 처음 본 순간 완전 딱 □인걸", "answer": "천생연분"},
    {"question": "부석순 <파이팅 해야지>\n우린 다 □ 꽂은 Zombie\n필요해 모두 다 텐션 Up pumpin’", "answer": "이어폰"},
    {"question": "박재정 <헤어지자 말해요>\n그대 이제 날 떠난다 말해요\n잠시라도 이 □을 느껴서 고마웠다고", "answer": "행복"},
    {"question": "방탄소년단 <봄날>\n이 순간 흐르는 □조차 미워\n우리가 변한 거지 뭐", "answer": "시간"},
    {"question": "아이브 <해야>\n못 기다린대 못 돼버린 내 맘이\n겁 따윈 없는 척하지 마 너 □", "answer": "감히"},
    {"question": "윤하 <사건의 지평선>\n노력은 우리에게 정답이 아니라서\n마지막 선물은 산뜻한 □", "answer": "안녕"}
]

@app.route('/')
def index():
    session['answered_count'] = 0  # 문제를 푼 횟수 초기화
    session['correct_count'] = 0  # 맞춘 정답 수 초기화
    session['question_pool'] = random.sample(questions, len(questions))  # 문제를 무작위로 섞어 풀 생성
    return render_template('index.html')

@app.route('/get_question', methods=['GET'])
def get_question():
    if session['answered_count'] >= 10:
        # 10문제를 다 풀면 결과 화면으로 리다이렉트
        return jsonify({"end": True, "correct_count": session['correct_count']})
    
    # 문제 풀에서 하나의 문제를 추출
    question = session['question_pool'].pop()
    session['current_answer'] = question['answer']  # 현재 문제의 정답 저장
    return jsonify({"question": question['question'], "end": False})

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get("answer", "").strip()  # 사용자의 입력 정답
    correct_answer = session['current_answer']  # 현재 문제의 정답

    # 사용자의 정답이 맞는지 확인
    is_correct = user_answer.lower() == correct_answer.lower()
    session['answered_count'] += 1  # 푼 문제 수 증가

    if is_correct:
        session['correct_count'] += 1  # 맞춘 정답 수 증가

    return jsonify({"result": is_correct, "correct_answer": correct_answer})

@app.route('/result')
def result():
    # 결과 페이지로 이동
    correct_count = session.get('correct_count', 0)
    incorrect_count = 10 - correct_count
    return render_template('result.html', correct_count=correct_count, incorrect_count=incorrect_count)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

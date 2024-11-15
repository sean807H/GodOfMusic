from flask import render_template, session
import random

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

def game():
    session['answered_count'] = 0  # 문제를 푼 횟수 초기화
    session['correct_count'] = 0  # 맞춘 정답 수 초기화
    session['question_pool'] = random.sample(questions, len(questions))  # 문제를 무작위로 섞어 풀 생성
    return render_template('game.html')
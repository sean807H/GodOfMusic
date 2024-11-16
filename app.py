from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_bytes(16)  # 비밀 키 설정

# 데이터 리스트
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

explain = [
    {"question": "세븐틴\n시련과 좌절을 겪으며 무한성장 중인 세븐틴을 표현한\n강렬한 메시지가 특징이다.", "answer": "손오공"},
    {"question": "TWS (투어스)\n첫 만남의 설렘 속 막연함을 앞으로의 빛나는\n날들에 대한 기대감으로 극복하는 이야기.", "answer": "첫 만남은 계획대로 되지않아"},
    {"question": "오마이걸\n친구에게 설렘을 느끼는 상황을 보드게임에 표현한\n가사가 인상적이다.", "answer": "살짝 설렜어"},
    {"question": "스트레이 키즈\n '애들 중 가장 별나고, 애들 중 가장 빛난다'는\n메시지를 담아 여러 곡이 합쳐진 듯한 구성이며,\n중독적인 리듬의 훅이 특징이다.", "answer": "특"},
    {"question": "볼빨간사춘기\n바쁜 일상 속 자유롭게 떠나고 싶은 마음을 담은 곡이다.", "answer": "여행"},
    {"question": "EXO (엑소)\n떠나 보낸 첫사랑을 떠올리며 지난 시간을 되돌리고\n싶은 마음을 담은 어쿠스틱 팝곡.", "answer": "첫 눈"},
    {"question": "스테이씨\n순수하게 봐주길 바라는 마음을 담았고, 감각적인\nBRASS 사운드를 통해 상큼하면서 우아한 분위기를 표현.", "answer": "색안경"},
    {"question": "여자친구\n달 구경하는 시간으로 사랑하는 사람을 떠올리는\n의미를 담은 아름다운 타이틀곡.", "answer": "밤"},
    {"question": "엔믹스\n그루비한 리듬 기반의 올드스쿨 힙합과 컨트리\n장르가 어우러진 MIXX POP.", "answer": "별별별"},
    {"question": "지코\n유행과 상관없이 빛나는 개성을 담은 곡으로 강렬한\n비트와 중독적인 훅이 특징이다.", "answer": "새삥"}
]

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

# 라우트 함수
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/choice')
def choice():
    return render_template('choice.html')

@app.route('/another_quiz')
def another_quiz():
    return redirect(url_for('choice'))



@app.route('/game')
def show_game():
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['question_pool'] = random.sample(questions, len(questions))
    session['quiz_type'] = 'lyrics'  # 'lyrics' 퀴즈 타입 설정
    return render_template('game.html')

@app.route('/explain')
def show_explain():
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['question_pool'] = random.sample(explain, len(explain))
    session['quiz_type'] = 'title'  # 'title' 퀴즈 타입 설정
    return render_template('explain.html')

@app.route('/songquiz', strict_slashes=False)  # 슬래시에 대한 엄격한 구분 해제
def show_songquiz():
    session.clear()
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['seen_questions'] = []
    session['quiz_type'] = 'karaoke'

    # 첫 번째 노래 가져오기
    current_song = get_new_song_question()
    session["current_song"] = current_song

    return render_template('songquiz.html', audio_file=current_song["audio"])

def get_new_song_question():
    seen_questions = session.get("seen_questions", [])
    remaining_questions = [q for q in songquiz_data if q["audio"] not in seen_questions]

    if not remaining_questions:
        session['seen_questions'] = []
        remaining_questions = songquiz_data[:]

    question = random.choice(remaining_questions)
    seen_questions.append(question["audio"])
    session["seen_questions"] = seen_questions

    return question

@app.route('/mvquiz', strict_slashes=False)  # 슬래시에 대한 엄격한 구분 해제
def show_mvquiz():
    session.clear()
    session['answered_count'] = 0
    session['correct_count'] = 0
    session['used_questions'] = []
    session['quiz_type'] = 'music_video'

    # 첫 번째 장면 가져오기
    current_scene = get_new_mv_question()
    session['current_question'] = current_scene

    return render_template('mvquiz.html', scene=current_scene)

def get_new_mv_question():
    used_questions = session.get('used_questions', [])
    remaining_questions = [q for q in mvquiz_data if q['image'] not in used_questions]
    if not remaining_questions:
        session['used_questions'] = []
        remaining_questions = mvquiz_data[:]
    question = random.choice(remaining_questions)
    used_questions.append(question['image'])
    session['used_questions'] = used_questions
    return question


@app.route('/restart_quiz/<quiz_type>')
def restart_quiz(quiz_type):
    session.clear()
    if quiz_type == 'lyrics':
        return redirect(url_for('show_game'))
    elif quiz_type == 'title':
        return redirect(url_for('show_explain'))
    elif quiz_type == 'karaoke':
        return redirect(url_for('show_songquiz'))
    elif quiz_type == 'music_video':
        return redirect(url_for('show_mvquiz'))
    else:
        return redirect(url_for('choice'))  # 기본적으로 메인 페이지로 리디렉션
    
# '/quiz' 라우트 추가
@app.route('/quiz')
def quiz():
    quiz_type = session.get('quiz_type', 'lyrics')

    if quiz_type == 'karaoke':
        if session['answered_count'] >= 10:
            return jsonify({"endQuiz": True})  # 마지막 문제일 경우 endQuiz 플래그 설정

        question = get_new_song_question()
        session["current_song"] = question
        return jsonify({
            "audio_file": question["audio"],
            "endQuiz": False
        })
    else:
        return jsonify({"error": "Invalid quiz type"}), 400

# '/load_next_question' 라우트 추가
@app.route('/load_next_question')
def load_next_question():
    quiz_type = session.get('quiz_type', 'lyrics')

    if quiz_type == 'music_video':
        if session['answered_count'] >= 10:
            return jsonify({"endQuiz": True})

        question = get_new_mv_question()
        session["current_question"] = question
        return jsonify({
            "image": question["image"],
            "endQuiz": False
        })
    else:
        return jsonify({"error": "Invalid quiz type"}), 400

@app.route('/get_question', methods=['GET'])
def get_question():
    quiz_type = session.get('quiz_type', 'lyrics')

    if quiz_type == 'karaoke':
        if session['answered_count'] >= 10:
            return jsonify({"endQuiz": True})
        question = get_new_song_question()
        session["current_song"] = question
        return jsonify({
            "audio_file": question["audio"],
            "endQuiz": False
        })
    elif quiz_type == 'music_video':
        if session['answered_count'] >= 10:
            return jsonify({"endQuiz": True})
        question = get_new_mv_question()
        session["current_question"] = question
        return jsonify({
            "image": question["image"],
            "endQuiz": False
        })
    else:
        # 기존의 처리 (lyrics, title)
        if session['answered_count'] >= 10:
            # 퀴즈가 끝났을 때 결과 페이지로 이동하면서 현재 퀴즈 타입을 전달
            return jsonify({"end": True, "correct_count": session['correct_count'], "quiz_type": quiz_type})
        
        question = session['question_pool'].pop()
        session['current_answer'] = question['answer']
        session['current_question'] = question  # 현재 질문을 세션에 저장

        response_data = {"end": False}

        if quiz_type == 'lyrics' or quiz_type == 'title':
            response_data["question"] = question['question']
        else:
            response_data["error"] = "Unknown quiz type"

        return jsonify(response_data)

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.json
    user_answer = data.get("answer", "").strip().lower()
    quiz_type = session.get('quiz_type', 'lyrics')

    if quiz_type == 'karaoke':
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
    elif quiz_type == 'music_video':
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
    else:
        # 기존의 처리 (lyrics, title)
        correct_answer = session['current_answer']
        # 여러 개의 정답이 있을 경우 처리
        correct_answers = [ans.strip().lower() for ans in correct_answer.split(',')]

        is_correct = user_answer in correct_answers
        session['answered_count'] += 1

        if is_correct:
            session['correct_count'] += 1

        response_data = {"result": is_correct, "correct_answer": correct_answer}

        return jsonify(response_data)

@app.route('/result')
def result():
    correct_count = session.get('correct_count', 0)
    incorrect_count = 10 - correct_count

    # 현재 퀴즈 타입을 세션에서 가져옴 (기본값은 'lyrics')
    quiz_type = session.get('quiz_type', 'lyrics')

    return render_template('result.html', correct_count=correct_count, incorrect_count=incorrect_count, quiz_type=quiz_type)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

from flask import Flask, render_template
from game import lyrics_quiz   # game.py의 lyrics_quiz 함수 가져오기
from explain import title_quiz # explain.py의 title_quiz 함수 가져오기

app = Flask(__name__)

@app.route('/')
def choice():
    return render_template('choice.html')

# 다른 Python 파일에서 정의된 함수를 직접 라우트로 연결
@app.route('/lyrics_quiz')
def show_lyrics_quiz():
    return lyrics_quiz()

@app.route('/title_quiz')
def show_title_quiz():
    return title_quiz()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=True)

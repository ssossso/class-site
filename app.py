from flask import Flask, request
import random
import string
import json
import os

app = Flask(__name__)

DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def make_class_code():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

@app.route("/")
def home():
    return """
    <h1>학급 사이트</h1>
    <a href='/teacher'>교사 로그인</a><br>
    <a href='/student'>학생 입장</a>
    """

@app.route("/teacher", methods=["GET", "POST"])
def teacher():
    if request.method == "POST":
        students_text = request.form["students"]
        students = [s.strip() for s in students_text.split(",") if s.strip()]

        data = load_data()
        code = make_class_code()
        data[code] = students
        save_data(data)

        return f"""
        <h2>학급 생성 완료</h2>
        <p>학급 코드: <b>{code}</b></p>
        <p>학생 수: {len(students)}명</p>
        <a href='/'>홈으로</a>
        """

    return """
    <h2>교사 - 학급 생성</h2>
    <form method="post">
        학생 이름 (쉼표로 구분)<br>
        <textarea name="students" rows="5" cols="40"></textarea><br><br>
        <button type="submit">학급 만들기</button>
    </form>
    """

@app.route("/student", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        code = request.form["code"].upper()
        data = load_data()

        if code not in data:
            return "<p>잘못된 학급 코드입니다.</p><a href='/student'>다시 입력</a>"

        students = data[code]
        student_list = "".join(f"<li>{s}</li>" for s in students)

        return f"""
        <h2>학생 명단</h2>
        <ul>{student_list}</ul>
        <a href='/'>홈으로</a>
        """

    return """
    <h2>학생 - 학급 입장</h2>
    <form method="post">
        학급 코드<br>
        <input name="code">
        <button type="submit">입장</button>
    </form>
    """

if __name__ == "__main__":
    app.run()

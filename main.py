import flet as ft
from ai_engine import generate_questions, evaluate_answer
from resume import read_resume
from database import init_db, save_interview, load_history

def main(page: ft.Page):
    page.title = "AI Interview Coach"
    page.scroll = "auto"

    init_db()

    questions = []
    index = 0
    role = ""
    total_score = 0

    role_input = ft.TextField(label="Job Role (e.g. HR, Data Scientist)")
    resume_text = ""

    question_text = ft.Text("")
    answer_input = ft.TextField(label="Your Answer", multiline=True)
    status = ft.Text()

    history_col = ft.Column()

    def refresh_history():
        history_col.controls.clear()
        for r, s, d in load_history():
            history_col.controls.append(
                ft.Text(f"{d} | {r} | {s}")
            )
        page.update()

    def upload_resume(e):
        nonlocal resume_text
        resume_text = read_resume(e.files[0].path)
        status.value = "Resume uploaded"
        page.update()

    def start_interview(e):
        nonlocal questions, index, role, total_score
        role = role_input.value
        questions = generate_questions(resume_text, role)
        index = 0
        total_score = 0
        question_text.value = questions[index]
        status.value = "Interview started"
        page.update()

    def submit_answer(e):
        nonlocal index, total_score
        feedback = evaluate_answer(
            questions[index],
            answer_input.value,
            role
        )
        total_score += 1
        index += 1
        answer_input.value = ""

        if index < len(questions):
            question_text.value = questions[index]
        else:
            save_interview(role, f"{total_score}/5")
            question_text.value = "Interview completed"
            refresh_history()

        page.update()

    page.add(
        role_input,
        ft.ElevatedButton("Upload Resume", on_click=lambda _: page.pick_files(on_result=upload_resume)),
        ft.ElevatedButton("Start Interview", on_click=start_interview),
        question_text,
        answer_input,
        ft.ElevatedButton("Submit", on_click=submit_answer),
        status,
        ft.Text("Interview History"),
        history_col
    )

    refresh_history()

ft.app(target=main)

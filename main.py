import flet as ft
from ai_engine import generate_questions, evaluate_answer
from resume import read_resume
from database import init_db, save_interview, load_history


def main(page: ft.Page):
    page.title = "AI Interview Coach"
    page.scroll = "auto"

    # ---------- INIT ----------
    init_db()

    questions = []
    current_index = 0
    total_score = 0
    role = ""
    resume_text = ""

    # ---------- FILE PICKER (FIXED) ----------
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    # ---------- UI CONTROLS ----------
    role_input = ft.TextField(
        label="Job Role (e.g. HR, Data Scientist)",
        width=400
    )

    question_text = ft.Text(size=16, weight="bold")
    answer_input = ft.TextField(
        label="Your Answer",
        multiline=True,
        min_lines=3,
        max_lines=6,
        width=500
    )

    status_text = ft.Text()
    history_column = ft.Column()

    # ---------- FUNCTIONS ----------
    def refresh_history():
        history_column.controls.clear()
        for r, s, d in load_history():
            history_column.controls.append(
                ft.Text(f"{d} | {r} | Score: {s}")
            )
        page.update()

    def upload_resume(e: ft.FilePickerResultEvent):
        nonlocal resume_text
        if e.files:
            resume_text = read_resume(e.files[0].path)
            status_text.value = "✅ Resume uploaded successfully"
            page.update()

    file_picker.on_result = upload_resume

    def start_interview(e):
        nonlocal questions, current_index, total_score, role
        role = role_input.value.strip()

        if not role:
            status_text.value = "❌ Please enter job role"
            page.update()
            return

        questions = generate_questions(resume_text, role)
        current_index = 0
        total_score = 0

        question_text.value = questions[current_index]
        status_text.value = "✅ Interview started"
        page.update()

    def submit_answer(e):
        nonlocal current_index, total_score

        if current_index >= len(questions):
            return

        feedback = evaluate_answer(
            questions[current_index],
            answer_input.value,
            role
        )

        total_score += 1
        answer_input.value = ""

        current_index += 1

        if current_index < len(questions):
            question_text.value = questions[current_index]
        else:
            save_interview(role, f"{total_score}/{len(questions)}")
            question_text.value = "🎉 Interview completed"
            status_text.value = "Results saved"
            refresh_history()

        page.update()

    # ---------- BUTTONS ----------
    upload_btn = ft.ElevatedButton(
        "Upload Resume (PDF)",
        on_click=lambda _: file_picker.pick_files(
            allow_multiple=False,
            allowed_extensions=["pdf"]
        )
    )

    start_btn = ft.ElevatedButton(
        "Start Interview",
        on_click=start_interview
    )

    submit_btn = ft.ElevatedButton(
        "Submit Answer",
        on_click=submit_answer
    )

    # ---------- PAGE LAYOUT ----------
    page.add(
        ft.Text("🤖 AI Interview Coach", size=22, weight="bold"),
        role_input,
        upload_btn,
        start_btn,
        ft.Divider(),
        question_text,
        answer_input,
        submit_btn,
        status_text,
        ft.Divider(),
        ft.Text("📊 Interview History", weight="bold"),
        history_column
    )

    refresh_history()


ft.app(target=main)

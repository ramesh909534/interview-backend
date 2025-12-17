import flet as ft
from ai_engine import generate_questions, evaluate_answer
from resume import read_resume
from database import save_interview, load_history
from datetime import datetime


def main(page: ft.Page):
    page.title = "AI Interview Coach"
    page.scroll = ft.ScrollMode.AUTO

    # ---------- STATE ----------
    page.session.set("resume_text", "")
    page.session.set("questions", [])
    page.session.set("current_index", 0)
    page.session.set("score", 0)

    # ---------- UI CONTROLS ----------
    role_input = ft.TextField(
        label="Job Role (e.g. HR, Data Scientist)",
        width=400
    )

    answer_input = ft.TextField(
        label="Your Answer",
        multiline=True,
        min_lines=4,
        width=600
    )

    status_text = ft.Text("")
    question_text = ft.Text(size=16, weight=ft.FontWeight.BOLD)

    history_column = ft.Column()

    # ---------- FILE PICKER ----------
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def upload_resume(e: ft.FilePickerResultEvent):
        if not e.files:
            status_text.value = "❌ No file selected"
            page.update()
            return

        file = e.files[0]

        try:
            # Web / Windows
            if file.path:
                resume_text = read_resume(file.path)
            # Mobile APK
            elif hasattr(file, "bytes") and file.bytes:
                resume_text = read_resume(file.bytes)
            else:
                raise Exception("Unable to read file")

            page.session.set("resume_text", resume_text)
            status_text.value = "✅ Resume uploaded successfully"

        except Exception as ex:
            status_text.value = f"❌ Resume error: {ex}"

        page.update()

    file_picker.on_result = upload_resume

    # ---------- INTERVIEW ----------
    def start_interview(e):
        role = role_input.value.strip()
        resume_text = page.session.get("resume_text", "")

        if not role:
            status_text.value = "❌ Enter job role"
            page.update()
            return

        try:
            questions = generate_questions(role, resume_text)
            page.session.set("questions", questions)
            page.session.set("current_index", 0)
            page.session.set("score", 0)

            question_text.value = f"Q1. {questions[0]}"
            status_text.value = "✅ Interview started"
            answer_input.value = ""

        except Exception as ex:
            status_text.value = f"❌ Question error: {ex}"

        page.update()

    def submit_answer(e):
        questions = page.session.get("questions", [])
        index = page.session.get("current_index", 0)

        if index >= len(questions):
            return

        try:
            score, feedback = evaluate_answer(
                questions[index],
                answer_input.value
            )

            total = page.session.get("score") + score
            page.session.set("score", total)

            index += 1
            page.session.set("current_index", index)

            if index < len(questions):
                question_text.value = f"Q{index+1}. {questions[index]}"
                answer_input.value = ""
                status_text.value = f"Score: {total}"
            else:
                status_text.value = f"🎉 Interview finished! Final Score: {total}"
                save_interview(role_input.value, total)
                refresh_history()

        except Exception as ex:
            status_text.value = f"❌ Answer error: {ex}"

        page.update()

    # ---------- HISTORY ----------
    def refresh_history():
        history_column.controls.clear()
        for h in load_history():
            history_column.controls.append(
                ft.Text(f"{h[2]} | {h[0]} | {h[1]}/100")
            )

    refresh_history()

    # ---------- LAYOUT ----------
    page.add(
        ft.Column(
            [
                ft.Text("🤖 AI Interview Coach", size=22, weight=ft.FontWeight.BOLD),
                role_input,
                ft.ElevatedButton("Upload Resume (PDF)", on_click=lambda _: file_picker.pick_files()),
                ft.ElevatedButton("Start Interview", on_click=start_interview),
                status_text,
                ft.Divider(),
                question_text,
                answer_input,
                ft.ElevatedButton("Submit Answer", on_click=submit_answer),
                ft.Divider(),
                ft.Text("📊 Interview History", size=18, weight=ft.FontWeight.BOLD),
                history_column,
            ]
        )
    )


ft.app(target=main, view=ft.WEB_BROWSER)

import flet as ft
from ai_engine import generate_questions, evaluate_answer
from resume import read_resume
from database import init_db, save_interview, load_history
from voice import listen_answer

def main(page: ft.Page):
    page.title = "AI Interview Coach"
    page.scroll = ft.ScrollMode.AUTO
    page.padding = 20

    # INIT DB
    init_db()

    # STATE
    page.session.set("resume_text", "")
    page.session.set("questions", [])
    page.session.set("index", 0)
    page.session.set("score", 0)

    # UI
    role_input = ft.TextField(label="Job Role (e.g HR, Data Scientist)", width=400)
    question_text = ft.Text(size=16, weight=ft.FontWeight.BOLD)
    answer_input = ft.TextField(multiline=True, min_lines=4, width=600)
    status = ft.Text()
    feedback = ft.Text()
    history_col = ft.Column()

    # FILE PICKER
    file_picker = ft.FilePicker()
    page.overlay.append(file_picker)

    def upload_resume(e: ft.FilePickerResultEvent):
        try:
            if not e.files:
                return

            f = e.files[0]

            if f.path:
                resume_text = read_resume(f.path)
            elif f.bytes:
                resume_text = read_resume(f.bytes)
            else:
                resume_text = ""

            page.session.set("resume_text", resume_text)
            status.value = "✅ Resume uploaded"

        except:
            page.session.set("resume_text", "")
            status.value = "⚠️ Resume ignored"

        page.update()

    file_picker.on_result = upload_resume

    def start_interview(e):
        role = role_input.value.strip()
        resume_text = page.session.get("resume_text", "")

        if not role:
            status.value = "❌ Enter job role"
            page.update()
            return

        questions = generate_questions(role, resume_text)
        if not questions:
            status.value = "❌ Unable to generate questions"
            page.update()
            return

        page.session.set("questions", questions)
        page.session.set("index", 0)
        page.session.set("score", 0)

        question_text.value = questions[0]
        answer_input.value = ""
        feedback.value = ""
        status.value = "✅ Interview started"
        page.update()

    def submit_answer(e):
        questions = page.session.get("questions")
        index = page.session.get("index")

        if index >= len(questions):
            return

        score, fb = evaluate_answer(questions[index], answer_input.value)
        total = page.session.get("score") + score

        page.session.set("score", total)
        feedback.value = fb
        index += 1
        page.session.set("index", index)

        if index < len(questions):
            question_text.value = questions[index]
            answer_input.value = ""
        else:
            final_score = int((total / (len(questions) * 10)) * 100)
            question_text.value = f"🎉 Interview Completed!\nScore: {final_score}/100"
            save_interview(role_input.value, final_score)
            refresh_history()

        page.update()

    def speak(e):
        answer_input.value = listen_answer()
        page.update()

    def refresh_history():
        history_col.controls.clear()
        for r, s, d in load_history():
            history_col.controls.append(
                ft.Text(f"{d} | {r} | {s}/100")
            )

    refresh_history()

    # LAYOUT
    page.add(
        ft.Text("🤖 AI Interview Coach", size=22, weight=ft.FontWeight.BOLD),
        role_input,
        ft.ElevatedButton("Upload Resume (PDF)", on_click=lambda _: file_picker.pick_files()),
        ft.ElevatedButton("Start Interview", on_click=start_interview),
        status,
        ft.Divider(),
        question_text,
        answer_input,
        ft.Row([
            ft.ElevatedButton("Submit", on_click=submit_answer),
            ft.ElevatedButton("🎤 Speak", on_click=speak)
        ]),
        feedback,
        ft.Divider(),
        ft.Text("📊 Interview History", size=18, weight=ft.FontWeight.BOLD),
        history_col
    )

ft.app(target=main)

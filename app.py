from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
import io
from database import init_db, save_interview, load_history
from ai_engine import generate_questions, evaluate_answer

app = FastAPI()
init_db()

@app.post("/upload_resume")
def upload_resume(file: UploadFile = File(...)):
    reader = PdfReader(io.BytesIO(file.file.read()))
    text = ""
    for p in reader.pages:
        if p.extract_text():
            text += p.extract_text()
    return {"resume": text}

@app.post("/generate")
def generate(data: dict):
    return {"questions": generate_questions(data["role"], data["resume"])}

@app.post("/evaluate")
def evaluate(data: dict):
    score, fb = evaluate_answer(data["question"], data["answer"])
    return {"score": score, "feedback": fb}

@app.post("/save")
def save(data: dict):
    save_interview(data["role"], data["score"])
    return {"status": "saved"}

@app.get("/history")
def history():
    return load_history()

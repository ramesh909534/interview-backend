from fastapi import FastAPI, UploadFile, File
from ai_engine import generate_questions, evaluate_answer
from resume import read_resume
from database import init_db, save_interview, load_history

app = FastAPI()
init_db()

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    data = await file.read()
    return {"resume_text": read_resume(data)}

@app.post("/generate")
def gen(data: dict):
    return {"questions": generate_questions(data["role"], data.get("resume",""))}

@app.post("/evaluate")
def eval(data: dict):
    return evaluate_answer(data["question"], data["answer"])

@app.post("/save_interview")
def save(data: dict):
    save_interview(data["role"], data["score"])
    return {"status": "ok"}

@app.get("/history")
def history():
    return load_history()

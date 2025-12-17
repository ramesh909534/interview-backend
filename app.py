from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.get("/")
def root():
    return {"status": "AI Interview Backend is running"}

class GenerateRequest(BaseModel):
    role: str
    resume: str = ""

class EvaluateRequest(BaseModel):
    question: str
    answer: str

@app.post("/generate")
def generate(req: GenerateRequest):
    prompt = f"""
You are an interviewer.
Job role: {req.role}
Resume: {req.resume}

Generate exactly 5 interview questions.
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    text = res.choices[0].message.content
    questions = [q.strip("-0123456789. ") for q in text.splitlines() if q.strip()]

    return {"questions": questions}

@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    prompt = f"""
Question: {req.question}
Answer: {req.answer}

Give:
Score out of 10
Short feedback
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    text = res.choices[0].message.content

    score = 5
    for line in text.splitlines():
        if "score" in line.lower():
            try:
                score = int("".join(filter(str.isdigit, line)))
            except:
                pass

    return {"score": score, "feedback": text}

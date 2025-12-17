from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI(title="AI Interview Backend")

@app.get("/")
def root():
    return {"status": "Backend running"}

class GenerateRequest(BaseModel):
    role: str
    resume: str = ""

class EvaluateRequest(BaseModel):
    question: str
    answer: str

@app.post("/generate")
def generate(req: GenerateRequest):
    try:
        prompt = f"""
You are an interviewer.
Job role: {req.role}
Resume: {req.resume}

Generate exactly 5 interview questions.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )

        text = response.choices[0].message["content"]
        questions = [
            q.strip("-0123456789. ")
            for q in text.splitlines()
            if q.strip()
        ]

        return {"questions": questions}

    except Exception as e:
        print("GENERATE ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    try:
        prompt = f"""
Question: {req.question}
Answer: {req.answer}

Give score (0-10) and short feedback.
"""

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        text = response.choices[0].message["content"]

        score = 5
        for line in text.splitlines():
            if "score" in line.lower():
                try:
                    score = int("".join(filter(str.isdigit, line)))
                except:
                    pass

        return {"score": score, "feedback": text}

    except Exception as e:
        print("EVALUATE ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

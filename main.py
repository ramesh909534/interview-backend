from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Data(BaseModel):
    role: str
    question: str
    answer: str

@app.post("/evaluate")
def evaluate(data: Data):
    prompt = f"""
You are an interview coach.

Job role: {data.role}
Question: {data.question}
Answer: {data.answer}

Give score out of 10 and short feedback.
"""
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"result": res.choices[0].message.content}

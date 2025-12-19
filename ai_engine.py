import requests, os, json

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

def generate_questions(role, resume):
    prompt = f"""
You are a recruiter.
Generate 5 interview questions for role: {role}.
Use resume if useful.

Resume:
{resume}
"""
    r = requests.post(API_URL, headers=HEADERS, json={
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    })
    text = r.json()["choices"][0]["message"]["content"]
    return [q.strip("- ") for q in text.split("\n") if q.strip()][:5]


def evaluate_answer(question, answer):
    prompt = f"""
Evaluate interview answer.

Question: {question}
Answer: {answer}

Return STRICT JSON:
{{
 "communication": 0,
 "technical": 0,
 "confidence": 0,
 "relevance": 0,
 "rating": 0,
 "strengths": "",
 "improvements": "",
 "ideal_answer": ""
}}
"""
    r = requests.post(API_URL, headers=HEADERS, json={
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    })
    return json.loads(r.json()["choices"][0]["message"]["content"])

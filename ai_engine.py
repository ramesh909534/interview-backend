import requests, os

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

def generate_questions(role, resume):
    prompt = f"Generate 5 interview questions for role {role}. Resume: {resume}"
    r = requests.post(API_URL, headers=HEADERS, json={
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    })
    text = r.json()["choices"][0]["message"]["content"]
    return [q for q in text.split("\n") if q.strip()]

def evaluate_answer(question, answer):
    prompt = f"Question: {question}\nAnswer: {answer}\nGive score (0-10) and feedback."
    r = requests.post(API_URL, headers=HEADERS, json={
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}]
    })
    text = r.json()["choices"][0]["message"]["content"]
    return 7, text

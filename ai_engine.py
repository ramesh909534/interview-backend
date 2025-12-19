import requests, os, json

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

def evaluate_answer(question, answer):
    prompt = f"""
You are an interview evaluator.

Question:
{question}

Candidate Answer:
{answer}

Evaluate on:
1. Communication (0-10)
2. Technical knowledge (0-10)
3. Confidence (0-10)
4. Relevance (0-10)

Give:
- Scores
- Overall rating out of 5 stars
- What candidate did well
- What to improve
- Ideal sample answer

Return STRICT JSON like:
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

    text = r.json()["choices"][0]["message"]["content"]

    return json.loads(text)

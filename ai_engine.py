import requests
import os

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

MODEL = "openai/gpt-3.5-turbo"

# ---------- LANGUAGE SUPPORT ----------
LANG = "en"

LANG_PROMPT = {
    "en": "Respond in English.",
    "ta": "Respond in Tamil language.",
    "hi": "Respond in Hindi language."
}

# 🔒 HOSPITAL DOMAIN ROLES
ALLOWED_ROLES = [
    "Doctor",
    "Nurse",
    "Staff Nurse",
    "Surgeon",
    "Physician",
    "Lab Technician",
    "Radiologist",
    "Pharmacist",
    "Medical Officer",
    "Hospital Administrator",
    "Receptionist",
    "Ward Boy",
    "Physiotherapist",
    "Anesthesiologist",
    "Cardiologist",
    "Neurologist",
    "Dentist",
    "Emergency Technician"
]


# =====================================================
# INTERNAL AI CALL
# =====================================================
def _call_ai(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=30
    )

    if r.status_code != 200:
        raise RuntimeError("AI service failed")

    data = r.json()
    return data["choices"][0]["message"]["content"]


# =====================================================
# GENERATE QUESTIONS
# =====================================================
def generate_questions(role: str, resume: str):
    try:
        role_text = role.strip()

        if not any(r.lower() in role_text.lower() for r in ALLOWED_ROLES):
            return []

        lang_instruction = LANG_PROMPT.get(LANG, "")

        prompt = (
            "Generate 5 professional hospital interview questions.\n"
            "Questions must be relevant to hospital / healthcare environment.\n\n"
            f"Hospital Job role: {role}\n"
            f"Candidate resume:\n{resume}\n\n"
            f"{lang_instruction}\n"
            "Return each question in a new line."
        )

        text = _call_ai(prompt)

        questions = [q.strip() for q in text.split("\n") if q.strip()]
        return questions[:5]

    except Exception:
        return []


# =====================================================
# BASIC EVALUATION (AI TRANSLATION ENABLED)
# =====================================================
def evaluate_answer(question: str, answer: str):
    try:

        prompt = (
            "Hospital Interview Evaluation\n\n"

            "IMPORTANT:\n"
            "If the candidate answer is NOT in English, "
            "first translate it into English internally.\n"
            "Then evaluate the translated answer.\n\n"

            f"Interview Question:\n{question}\n\n"
            f"Candidate Answer:\n{answer}\n\n"

            "Evaluate answer relevance to hospital / healthcare role.\n"
            "Give:\n"
            "1) Score out of 10\n"
            "2) Short constructive feedback\n\n"

            "Format:\n"
            "Score: X\n"
            "Feedback: text"
        )

        text = _call_ai(prompt)

        score = 0
        feedback = text

        for line in text.split("\n"):
            if "score" in line.lower():
                digits = "".join(c for c in line if c.isdigit())
                if digits:
                    score = min(int(digits), 10)

        return score, feedback

    except Exception:
        return 0, "Evaluation failed"


# =====================================================
# ADVANCED HR EVALUATION
# =====================================================
def evaluate_hr_detailed(question: str, answer: str):
    try:

        prompt = (
            "Final HR Hospital Interview Evaluation\n\n"

            "IMPORTANT:\n"
            "If the candidate answer is not English, "
            "translate it to English first.\n\n"

            f"Final HR Interview Question:\n{question}\n\n"
            f"Candidate Answer:\n{answer}\n\n"

            "Provide detailed HR analysis including:\n"
            "- Communication\n"
            "- Confidence\n"
            "- Professionalism\n"
            "- Improvement suggestions\n"
        )

        return _call_ai(prompt)

    except Exception:
        return None


# =====================================================
# COMPATIBILITY WRAPPER
# =====================================================
def evaluate_detailed(question: str, answer: str):
    try:
        return evaluate_hr_detailed(question, answer)
    except Exception:
        return None

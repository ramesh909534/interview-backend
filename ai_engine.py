import requests
import os

API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

MODEL = "openai/gpt-3.5-turbo"

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
# INTERNAL AI CALL (DO NOT CHANGE)
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
# GENERATE QUESTIONS (HOSPITAL ONLY)
# =====================================================
def generate_questions(role: str, resume: str):
    """
    Hospital domain only.
    Old behavior preserved.
    """
    try:
        role_text = role.strip()

        # 🔒 Strict hospital validation
        if not any(r.lower() in role_text.lower() for r in ALLOWED_ROLES):
            return []

        if "Final HR" in role or "Negotiation" in role:
            prompt = (
                "You are an HR manager conducting the FINAL interview round "
                "for a hospital job role.\n"
                "Ask 5 realistic hospital HR + salary negotiation questions.\n"
                "Include salary expectation & negotiation questions relevant to hospital employment.\n\n"
                f"Hospital Job role: {role}\n"
                f"Candidate resume:\n{resume}\n\n"
                "Return each question in a new line."
            )
        else:
            prompt = (
                "Generate 5 professional hospital interview questions.\n"
                "Questions must be relevant to hospital / healthcare environment.\n\n"
                f"Hospital Job role: {role}\n"
                f"Candidate resume:\n{resume}\n\n"
                "Return each question in a new line."
            )

        text = _call_ai(prompt)
        questions = [q.strip() for q in text.split("\n") if q.strip()]
        return questions[:5]

    except Exception:
        return []


# =====================================================
# BASIC EVALUATION (UNCHANGED STRUCTURE)
# =====================================================
def evaluate_answer(question: str, answer: str):
    """
    Old API preserved
    Returns: (score:int, feedback:str)
    """
    try:
        is_salary = any(
            k in question.lower()
            for k in ["salary", "package", "ctc", "expectation", "negotiate"]
        )

        if is_salary:
            prompt = (
                "Hospital HR Interview Evaluation\n\n"
                f"HR Interview Question:\n{question}\n\n"
                f"Candidate Answer:\n{answer}\n\n"
                "Evaluate candidate on:\n"
                "- Confidence\n"
                "- Communication\n"
                "- Salary negotiation clarity\n"
                "- Professionalism in hospital setting\n\n"
                "Give:\n"
                "1) Score out of 10\n"
                "2) HR-style constructive feedback\n\n"
                "Format:\nScore: X\nFeedback: text"
            )
        else:
            prompt = (
                "Hospital Interview Evaluation\n\n"
                f"Interview Question:\n{question}\n\n"
                f"Candidate Answer:\n{answer}\n\n"
                "Evaluate answer relevance to hospital / healthcare role.\n"
                "Give:\n"
                "1) Score out of 10\n"
                "2) Short constructive feedback\n\n"
                "Format:\nScore: X\nFeedback: text"
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
# ADVANCED HR EVALUATION (HOSPITAL CONTEXT)
# =====================================================
def evaluate_hr_detailed(question: str, answer: str):
    """
    Recruiter-grade HR evaluation (Hospital version)
    """
    try:
        prompt = (
            "Final HR Hospital Interview Evaluation\n\n"
            f"Final HR Interview Question:\n{question}\n\n"
            f"Candidate Answer:\n{answer}\n\n"
            "Evaluate and provide:\n"
            "- Communication score (0-10)\n"
            "- Confidence score (0-10)\n"
            "- Salary negotiation skill (0-10)\n"
            "- Professional suitability for hospital environment (0-10)\n"
            "- Overall rating out of 5 stars\n"
            "- Final recommendation: Hire / Maybe / Reject\n"
            "- What candidate did well\n"
            "- What needs improvement\n"
            "- Ideal sample answer for hospital job\n\n"
            "Return response in clear readable text."
        )

        return _call_ai(prompt)

    except Exception:
        return None


# =====================================================
# 🔒 COMPATIBILITY WRAPPER (DO NOT REMOVE)
# =====================================================
def evaluate_detailed(question: str, answer: str):
    try:
        return evaluate_hr_detailed(question, answer)
    except Exception:
        return None
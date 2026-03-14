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
# LANGUAGE DETECTION
# =====================================================
def detect_language(text: str):

    tamil_chars = "அஆஇஈஉஊஎஏஐஒஓஔ"

    if any(c in text for c in tamil_chars):
        return "Tamil"

    return "English"


# =====================================================
# GENERATE QUESTIONS
# =====================================================
def generate_questions(role: str, resume: str):

    try:

        role_text = role.strip()

        if not any(r.lower() in role_text.lower() for r in ALLOWED_ROLES):
            return []

        language = detect_language(resume)

        if "Final HR" in role:

            prompt = f"""
You are a hospital HR interviewer.

Generate 5 FINAL ROUND hospital interview questions.

Include:
- Salary negotiation
- Career goals
- Hospital ethics
- Patient care responsibility

Language: {language}

Hospital Job Role:
{role}

Candidate Resume:
{resume}

Return each question in a new line.
"""

        else:

            prompt = f"""
Generate 5 professional hospital interview questions.

Rules:
- Must relate to healthcare environment
- Must match the candidate resume
- Questions must test real hospital experience

Language: {language}

Job Role:
{role}

Resume:
{resume}

Return each question on a new line.
"""

        text = _call_ai(prompt)

        questions = [
            q.strip()
            for q in text.split("\n")
            if q.strip()
        ]

        return questions[:5]

    except Exception:
        return []


# =====================================================
# BASIC ANSWER EVALUATION
# =====================================================
def evaluate_answer(question: str, answer: str):

    try:

        language = detect_language(answer)

        prompt = f"""
Hospital Interview Evaluation

Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer.

Check:
- Medical knowledge relevance
- Communication clarity
- Confidence
- Professional behaviour

Language: {language}

Give response format:

Score: X/10
Feedback: short improvement suggestion
"""

        text = _call_ai(prompt)

        score = 0
        feedback = text

        for line in text.split("\n"):

            if "score" in line.lower():

                digits = "".join(
                    c for c in line if c.isdigit()
                )

                if digits:
                    score = min(int(digits), 10)

        return score, feedback

    except Exception:

        return 0, "Evaluation failed"


# =====================================================
# IDEAL ANSWER GENERATOR
# =====================================================
def ideal_answer(question: str):

    try:

        prompt = f"""
Provide an ideal professional answer
for a hospital job interview.

Question:
{question}

Return a concise sample answer.
"""

        return _call_ai(prompt)

    except Exception:

        return "Ideal answer unavailable"


# =====================================================
# RESUME SKILL EXTRACTION
# =====================================================
def extract_skills(resume: str):

    try:

        prompt = f"""
Extract key medical skills from this resume.

Resume:
{resume}

Return a simple list of skills.
"""

        return _call_ai(prompt)

    except Exception:

        return "Skill extraction failed"


# =====================================================
# ADVANCED HR EVALUATION
# =====================================================
def evaluate_hr_detailed(question: str, answer: str):

    try:

        prompt = f"""
Final HR Hospital Interview Evaluation

Question:
{question}

Candidate Answer:
{answer}

Evaluate and provide:

- Communication score (0-10)
- Confidence score (0-10)
- Technical knowledge (0-10)
- Professional behaviour (0-10)
- Overall rating (5 stars)
- Hire decision: Hire / Maybe / Reject
- Improvement suggestions

Return readable text.
"""

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
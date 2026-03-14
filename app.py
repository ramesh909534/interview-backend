from fastapi import FastAPI, UploadFile, File, HTTPException
from pypdf import PdfReader
import io

from database import (
    init_db,
    save_interview,
    load_history,
    save_analytics,
    load_latest_analytics
)

from ai_engine import (
    generate_questions,
    evaluate_answer,
    evaluate_detailed,
    ideal_answer,
    extract_skills
)

app = FastAPI(
    title="🏥 Hospital AI Interview Backend",
    version="2.0"
)

# ---------- INIT DATABASE ----------
init_db()


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
# HEALTH CHECK
# =====================================================
@app.get("/")
async def health():
    return {"status": "Hospital AI Interview API running"}


# =====================================================
# RESUME UPLOAD
# =====================================================
@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):

    try:

        contents = await file.read()

        reader = PdfReader(io.BytesIO(contents))

        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return {
            "resume_text": text.strip()
        }

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Resume parsing failed"
        )


# =====================================================
# GENERATE QUESTIONS
# =====================================================
@app.post("/generate")
async def generate(data: dict):

    try:

        role = data.get("role", "").strip()

        if not role:

            raise HTTPException(
                status_code=400,
                detail="Role required"
            )

        # 🔒 Hospital validation
        if not any(r.lower() in role.lower() for r in ALLOWED_ROLES):

            raise HTTPException(
                status_code=403,
                detail="Only hospital domain job roles allowed"
            )

        questions = generate_questions(
            role,
            data.get("resume", "")
        )

        return {
            "questions": questions
        }

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Question generation failed"
        )


# =====================================================
# EVALUATE ANSWER
# =====================================================
@app.post("/evaluate")
async def evaluate(data: dict):

    try:

        question = data.get("question", "")
        answer = data.get("answer", "")

        score, feedback = evaluate_answer(
            question,
            answer
        )

        return {
            "score": score,
            "feedback": feedback
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Evaluation failed"
        )


# =====================================================
# IDEAL ANSWER
# =====================================================
@app.post("/ideal_answer")
async def ideal(data: dict):

    try:

        question = data.get("question", "")

        if not question:

            raise HTTPException(
                status_code=400,
                detail="Question required"
            )

        answer = ideal_answer(question)

        return {
            "ideal_answer": answer
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Ideal answer generation failed"
        )


# =====================================================
# SKILL EXTRACTION
# =====================================================
@app.post("/extract_skills")
async def skills(data: dict):

    try:

        resume = data.get("resume", "")

        skills = extract_skills(resume)

        return {
            "skills": skills
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Skill extraction failed"
        )


# =====================================================
# SAVE INTERVIEW
# =====================================================
@app.post("/save_interview")
async def save(data: dict):

    try:

        role = data.get("role")
        score = data.get("score")

        if not role:

            raise HTTPException(
                status_code=400,
                detail="Role required"
            )

        if not any(r.lower() in role.lower() for r in ALLOWED_ROLES):

            raise HTTPException(
                status_code=403,
                detail="Invalid role. Hospital jobs only."
            )

        save_interview(role, score)

        return {
            "status": "saved"
        }

    except HTTPException:
        raise

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Saving interview failed"
        )


# =====================================================
# INTERVIEW HISTORY
# =====================================================
@app.get("/history")
async def history():

    try:

        return load_history()

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Unable to load history"
        )


# =====================================================
# ADVANCED HR ANALYSIS
# =====================================================
@app.post("/evaluate_detailed")
async def evaluate_detailed_api(data: dict):

    try:

        result = evaluate_detailed(
            data.get("question", ""),
            data.get("answer", "")
        )

        if not result:
            raise ValueError

        return {
            "analysis": result
        }

    except Exception:

        raise HTTPException(
            status_code=500,
            detail="Detailed evaluation failed"
        )


# =====================================================
# SAVE ANALYTICS
# =====================================================
@app.post("/save_analytics")
async def save_analytics_api(data: dict):

    try:

        save_analytics(data)

        return {
            "status": "analytics_saved"
        }

    except Exception:

        raise HTTPException(
            status_code=400,
            detail="Saving analytics failed"
        )


# =====================================================
# ANALYTICS SUMMARY
# =====================================================
@app.get("/analytics_summary")
async def analytics_summary():

    data = load_latest_analytics()

    if not data:

        return {
            "communication": 6,
            "technical": 6,
            "confidence": 6,
            "relevance": 6,
            "negotiation": 5,
            "overall": 3.0,
            "recommendation": "Maybe"
        }

    return data
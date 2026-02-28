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
    evaluate_detailed
)

app = FastAPI(title="🏥 Hospital AI Interview Backend")

# ---------- INIT DB ----------
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
# ================= PHASE 1 APIs ======================
# =====================================================

@app.post("/upload_resume")
async def upload_resume(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        reader = PdfReader(io.BytesIO(contents))

        text = ""
        for p in reader.pages:
            extracted = p.extract_text()
            if extracted:
                text += extracted + "\n"

        return {"resume_text": text.strip()}

    except Exception:
        raise HTTPException(status_code=400, detail="Resume parsing failed")


@app.post("/generate")
async def generate(data: dict):
    try:
        role = data.get("role", "").strip()

        # 🔒 Strict hospital validation at API level
        if not any(r.lower() in role.lower() for r in ALLOWED_ROLES):
            raise HTTPException(
                status_code=403,
                detail="Only hospital domain job roles allowed"
            )

        questions = generate_questions(
            role,
            data.get("resume", "")
        )
        return {"questions": questions}

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Question generation failed")


@app.post("/evaluate")
async def evaluate(data: dict):
    try:
        score, feedback = evaluate_answer(
            data.get("question", ""),
            data.get("answer", "")
        )
        return {"score": score, "feedback": feedback}
    except Exception:
        raise HTTPException(status_code=500, detail="Evaluation failed")


@app.post("/save_interview")
async def save(data: dict):
    try:
        role = data["role"]

        # 🔒 Extra protection before saving
        if not any(r.lower() in role.lower() for r in ALLOWED_ROLES):
            raise HTTPException(
                status_code=403,
                detail="Invalid role. Hospital jobs only."
            )

        save_interview(role, data["score"])
        return {"status": "saved"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=400, detail="Saving interview failed")


@app.get("/history")
async def history():
    try:
        return load_history()
    except Exception:
        raise HTTPException(status_code=500, detail="Unable to load history")


# =====================================================
# ================= PHASE 2 APIs ======================
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

        return {"analysis": result}
    except Exception:
        raise HTTPException(status_code=500, detail="Detailed evaluation failed")


@app.post("/save_analytics")
async def save_analytics_api(data: dict):
    try:
        save_analytics(data)
        return {"status": "analytics_saved"}
    except Exception:
        raise HTTPException(status_code=400, detail="Saving analytics failed")


@app.get("/analytics_summary")
async def analytics_summary():
    """
    Used by hospital mobile dashboard
    """
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
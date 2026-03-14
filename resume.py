"""
resume.py

🏥 Hospital Interview Resume Parser
Advanced version with:
- Text extraction
- Email detection
- Phone detection
- Basic skill extraction
"""

from PyPDF2 import PdfReader
import io
import re


# =====================================================
# READ RESUME TEXT
# =====================================================
def read_resume(file_bytes: bytes) -> str:
    """
    Extracts raw text from PDF resume.
    """

    try:

        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in reader.pages:

            extracted = page.extract_text()

            if extracted:
                text += extracted + "\n"

        return clean_text(text)

    except Exception:

        return ""


# =====================================================
# CLEAN TEXT
# =====================================================
def clean_text(text: str):

    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =====================================================
# EMAIL EXTRACTION
# =====================================================
def extract_email(text: str):

    pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# =====================================================
# PHONE EXTRACTION
# =====================================================
def extract_phone(text: str):

    pattern = r"\+?\d[\d\s\-]{8,15}"

    match = re.search(pattern, text)

    if match:
        return match.group()

    return None


# =====================================================
# BASIC SKILL EXTRACTION
# =====================================================
MEDICAL_SKILLS = [
    "patient care",
    "clinical research",
    "nursing",
    "surgery",
    "radiology",
    "pharmacy",
    "diagnosis",
    "emergency care",
    "icu",
    "medical records",
    "laboratory",
    "anesthesia",
]


def extract_skills(text: str):

    found = []

    lower = text.lower()

    for skill in MEDICAL_SKILLS:

        if skill in lower:
            found.append(skill)

    return found


# =====================================================
# RESUME SUMMARY
# =====================================================
def parse_resume(file_bytes: bytes):
    """
    Full resume parser.
    Returns structured data.
    """

    text = read_resume(file_bytes)

    return {
        "text": text,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text),
    }
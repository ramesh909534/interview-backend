"""
resume.py

🏥 Hospital Interview Resume Parser

Used to extract text from uploaded PDF resumes.
Supports healthcare / hospital job applicants.
"""

from PyPDF2 import PdfReader
import io


def read_resume(file_bytes: bytes) -> str:
    """
    Extracts text from PDF resume.

    Used for hospital job interview question generation.
    """
    try:
        reader = PdfReader(io.BytesIO(file_bytes))
        text = ""

        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

        return text.strip()

    except Exception:
        # Safe fallback if resume parsing fails
        return ""
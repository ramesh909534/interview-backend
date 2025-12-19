from PyPDF2 import PdfReader
import io

def read_resume(file_bytes):
    reader = PdfReader(io.BytesIO(file_bytes))
    text = ""
    for p in reader.pages:
        text += p.extract_text() or ""
    return text.strip()

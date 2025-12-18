from PyPDF2 import PdfReader
import io

def read_resume(file):
    text = ""

    # 📄 If file path (desktop)
    if isinstance(file, str):
        reader = PdfReader(file)
    else:
        # 📱 Mobile bytes
        reader = PdfReader(io.BytesIO(file))

    for page in reader.pages:
        text += page.extract_text() or ""

    return text.strip()

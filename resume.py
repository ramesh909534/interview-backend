from pypdf import PdfReader
import io

def read_resume(source):
    """
    source = file path (Windows)
    source = bytes (Android APK)
    """
    text = ""

    try:
        if isinstance(source, str):
            reader = PdfReader(source)

        elif isinstance(source, (bytes, bytearray)):
            reader = PdfReader(io.BytesIO(source))

        else:
            return ""

        for page in reader.pages:
            t = page.extract_text()
            if t:
                text += t + "\n"

        return text.strip()

    except:
        return ""

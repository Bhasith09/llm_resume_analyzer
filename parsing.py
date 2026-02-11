# parsing.py
import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file) -> str:
    """
    Takes a Streamlit uploaded_file object (PDF) and returns extracted text.
    """
    pdf_bytes = uploaded_file.read()
    reader = PdfReader(io.BytesIO(pdf_bytes))
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from io import BytesIO

def create_pdf_report(text: str) -> bytes:
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)

    width, height = letter
    y = height - 50  # Start position

    pdf.setFont("Helvetica", 11)

    # Wrap long text safely
    lines = simpleSplit(text, "Helvetica", 11, width - 80)

    for line in lines:
        if y < 50:  # New page if needed
            pdf.showPage()
            pdf.setFont("Helvetica", 11)
            y = height - 50

        pdf.drawString(40, y, line)
        y -= 15

    pdf.save()
    buffer.seek(0)
    return buffer.read()

from fpdf import FPDF

def export_interview_session(history):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for item in history:
        # Encode text to latin-1 to avoid unicode errors in standard fpdf, or replace characters
        q = item.get('question', '').encode('latin-1', 'replace').decode('latin-1')
        a = item.get('answer', '').encode('latin-1', 'replace').decode('latin-1')
        f = item.get('feedback', '').encode('latin-1', 'replace').decode('latin-1')
        
        pdf.multi_cell(0, 10, f"Q: {q}")
        pdf.multi_cell(0, 10, f"A: {a}")
        pdf.multi_cell(0, 10, f"Feedback: {f}")
        pdf.ln(5)
    
    pdf.output("interview_session.pdf")

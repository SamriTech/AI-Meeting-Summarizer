from fpdf import FPDF
import datetime
import os

class MeetingReport(FPDF):
    def header(self):
        # Professional Blue Header
        self.set_fill_color(41, 128, 185)
        self.rect(0, 0, 210, 40, 'F')
        
        self.set_font("Helvetica", "B", 22)
        self.set_text_color(255, 255, 255)
        self.cell(0, 20, "AI MEETING SUMMARY", ln=True, align="C")
        
        self.set_font("Helvetica", "", 10)
        date_str = datetime.datetime.now().strftime("%B %d, %Y | %I:%M %p")
        self.cell(0, 5, f"Generated on: {date_str}", ln=True, align="C")
        self.ln(15)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

def generate_pdf(summary_text):
    pdf = MeetingReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # Body Styling
    pdf.set_font("Helvetica", size=11)
    pdf.set_text_color(44, 62, 80)
    
    # --- THE MAGIC BIT ---
    # markdown=True tells fpdf to render **bold** and *italics*
    # We use multi_cell to handle line breaks and margins automatically
    pdf.multi_cell(0, 7, txt=summary_text, markdown=True)
    
    # Save the file
    if not os.path.exists("reports"):
        os.makedirs("reports")
        
    file_path = "reports/Meeting_Summary.pdf"
    pdf.output(file_path)
    return file_path
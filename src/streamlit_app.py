import streamlit as st
from fpdf import FPDF
from pathlib import Path

st.set_page_config(page_title="שלב 3 – הפקת תג", layout="wide")
st.title("שלב 3 - הפקת תג")

if st.button("הפק PDF"):
    class PDF(FPDF):
        def header(self):
            logo_path = Path("impact_logo.png")
            if logo_path.exists():
                self.image(str(logo_path), x=30, y=10, w=150)
                self.ln(65)
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    lines = [
        "תעודה: הצהרת COC - מגש הדפסה",
        "1. אנו מצהירים שתעודת COC עבור מגש הדפסה מספר ________",
        "2. אנו מצהירים כי המגש הודפס ללקוח, נבחן ונבדק בהתאם להנחיות פנימיות ונמצא תקין...",
        "3. אנו מצהירים כי המגש נוקה, נבדק והוזן לאריזה לפי נוהל הארגון ולפי דרישות הלקוח.",
        "",
        "הערות: נא למלא פרטים של שרטוטים שנבדקו (או להוסיף כנספח אם נדרש)",
        "",
        "בתעודה נכלל:",
        "- בדיקת מגש הדפסה מכנית ע\"י מערכת ההדפסה",
        "- הדפסה בחומר גלם ניילון 12 (PA12)",
        "- טכנולוגיית הדפסה: SLS או MJF",
        "- מדפסת: HP Jet Fusion 5200",
        "- מצב הדפסה: Balanced Mode",
        "- הדפסה בצפיפות Infill 100% (חומר מלא)",
        "- הדפסה עם לפחות 20% חומר הדפסה חדש",
        "- סיום ההדפסה במצב ביצוע קירור טבעי (Optimal)",
        "- צביעה בשחור לכל החלקים",
        "- טיפול בגמר AMT לכל החלקים",
        "",
        "חתימת ספק:",
        "שם | תפקיד | חברה | תאריך | חתימה",
        "",
        "חתימת לקוח:",
        "שם | תפקיד | חברה | תאריך | חתימה"
    ]
    
    for line in lines:
        pdf.multi_cell(0, 10, txt=line)
    
    output_path = "tag_coc_output.pdf"
    pdf.output(output_path)
    with open(output_path, "rb") as f:
        st.download_button("📥 הורד PDF", f, file_name=output_path)


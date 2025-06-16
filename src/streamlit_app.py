import streamlit as st
from fpdf import FPDF
from pathlib import Path

st.set_page_config(page_title="Tag Generator - MJF", layout="wide")

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "שלב 1 - הזנת נתונים"

tabs = st.tabs(["שלב 1 - הזנת נתונים", "שלב 2 - שרטוטים ומידות", "שלב 3 - הפקת תג"])

# -- שלב 1 --
with tabs[0]:
    st.header("שלב 1 - הזנת נתונים")
    st.text_input("מספר אצווה", key="batch_number")
    st.text_input("שם פרויקט", key="project_name")
    st.text_input("שם לקוח", key="customer_name")

    if st.button("המשך לשלב הבא"):
        st.session_state.current_tab = "שלב 2 - שרטוטים ומידות"

# -- שלב 2 --
with tabs[1]:
    st.header("שלב 2 - שרטוטים ומידות")

    with st.expander("📁 העלה PDF של שרטוטים (אופציונלי)"):
        uploaded_pdf = st.file_uploader("בחר קובץ שרטוט PDF", type=["pdf"])
        num_criteria = st.number_input("מספר קריטריונים לבדיקה", min_value=0, step=1)

    functional_check = st.checkbox("בדיקה פונקציונלית", key="functional_check")
    go_nogo_check = st.checkbox("Go / No-Go", key="go_nogo_check")

    st.text_area("הערות בודק (אופציונלי)", key="qa_description")

    if st.button("המשך לשלב 3"):
        st.session_state.current_tab = "שלב 3 - הפקת תג"

# -- שלב 3 --
with tabs[2]:
    st.header("שלב 3 - הפקת תג")

    if st.button("הפק PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # הטמעת לוגו
        logo_path = Path(__file__).parent / "impact_logo.png"
        if logo_path.exists():
            pdf.image(str(logo_path), x=80, y=10, w=50)
            pdf.ln(40)  # רווח מתחת ללוגו

        pdf.cell(200, 10, txt="Usable Tag - Impact Labs", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Batch: {st.session_state.get('batch_number', '')}", ln=True)
        pdf.cell(200, 10, txt=f"Project: {st.session_state.get('project_name', '')}", ln=True)
        pdf.cell(200, 10, txt=f"Customer: {st.session_state.get('customer_name', '')}", ln=True)
        pdf.cell(200, 10, txt="QA Section:", ln=True)
        pdf.cell(200, 10, txt=f"Functional Check: {'Yes' if st.session_state.get('functional_check') else 'No'}", ln=True)
        pdf.cell(200, 10, txt=f"Go / No-Go: {'Yes' if st.session_state.get('go_nogo_check') else 'No'}", ln=True)
        pdf.multi_cell(0, 10, txt=f"QA Notes:\n{st.session_state.get('qa_description', '')}")

        output_path = "tag.pdf"
        pdf.output(output_path)

        st.success("התג הופק בהצלחה!")
        with open(output_path, "rb") as f:
            st.download_button("📥 הורד את הקובץ", f, file_name="tag.pdf")

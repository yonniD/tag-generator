import streamlit as st
from fpdf import FPDF
from pathlib import Path

st.set_page_config(page_title="מערכת ניהול צוות - MJF", layout="wide")

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "שלב 1 - הזנת אצווה"

tabs = st.tabs(["שלב 1 - הזנת אצווה", "שלב 2 - שרטוטים ומידות", "שלב 3 - הנפקת תג"])

# --- שלב 1 ---
with tabs[0]:
    st.header("📋 שלב 1 - הזנת אצווה")
    st.text_input("מספר אצווה", key="batch_number")
    st.text_input("שם פרויקט", key="project_name")
    st.text_input("שם לקוח", key="customer_name")
    if st.button("המשך לשלב הבא"):
        st.session_state.current_tab = "שלב 2 - שרטוטים ומידות"

# --- שלב 2 ---
with tabs[1]:
    st.header("📐 שלב 2 - שרטוטים ומידות")

    with st.expander("📄 לפי חלק להזנת בדיקות"):
        uploaded_pdf = st.file_uploader("העלה שרטוט PDF", type=["pdf"])
        num_criteria = st.number_input("מספר פריטי קריטיות", min_value=0, step=1)

        functional_check = st.checkbox("בדיקה פונקציונלית", key="functional_check")
        go_nogo_check = st.checkbox("Go / No-Go", key="go_nogo_check")

        st.text_area("תיאור הבדיקה (רשות)", key="qa_description")

    if st.button("המשך לשלב הבא", key="go_to_step_3"):
        st.session_state.current_tab = "שלב 3 - הנפקת תג"

# --- שלב 3 ---
with tabs[2]:
    st.header("🖨️ שלב 3 - הנפקת תג")
    if st.button("הפק PDF"):
        pdf = FPDF()
        pdf.add_page()

        # טען פונט בעברית (פעם אחת בלבד)
        pdf.add_font("FreeSans", "", "fonts/FreeSans.ttf", uni=True)
        pdf.set_font("FreeSans", size=14)

        pdf.cell(200, 10, txt="תג שמיש - Impact Labs", ln=True, align="C")

        pdf.output("tag.pdf")
        st.success("התג הופק בהצלחה!")
        with open("tag.pdf", "rb") as f:
            st.download_button("📥 הורד את ה-PDF", f, file_name="tag.pdf")

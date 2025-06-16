import streamlit as st

st.set_page_config(page_title="תג שמיש - MJF", layout="wide")

if "parts_data" not in st.session_state:
    st.session_state.parts_data = []

# 🟦 טאב 1 – אצווה
tab1, tab2, tab3 = st.tabs(["📦 הזנת אצווה", "📐 שרטוטים ומידות", "🧪 בקרת איכות QA"])

with tab1:
    st.header("📦 הזנת פרטי אצווה")
    col1, col2 = st.columns(2)

    with col1:
        printer_type = st.text_input("סוג מדפסת", "HP MJF 5200", disabled=True)
        job_id = st.text_input("Job ID")
        packing_density = st.number_input("Packing Density", step=0.01)
        print_date = st.date_input("תאריך ייצור")

    with col2:
        coa = st.text_input("COA")
        operator_name = st.text_input("שם מפעיל הדפסה")

    st.markdown("---")
    st.subheader("🧩 חלקים באצווה")

    num_parts = st.number_input("כמה סוגי חלקים יש באצווה?", min_value=1, step=1)

    st.session_state.parts_data = []
    for i in range(int(num_parts)):
        with st.expander(f"חלק {i+1}"):
            part_name = st.text_input(f"שם חלק #{i+1}", key=f"name_{i}")
            quantity = st.number_input(f"כמות חלקים מסוג זה", min_value=1, step=1, key=f"qty_{i}")
            st.session_state.parts_data.append((part_name, quantity))

    st.info("בסיום שלב זה, עבור לטאב הבא להזנת שרטוט ומידות ✏️")

# 🟨 טאב 2 – שרטוטים ומידות
with tab2:
    st.header("📐 הזנת שרטוטים ומידות קריטיות")

    for i, (part_name, quantity) in enumerate(st.session_state.parts_data):
        with st.expander(f"🔧 חלק: {part_name}"):
            uploaded_drawing = st.file_uploader(f"העלה שרטוט PDF עבור {part_name}", type=["pdf"], key=f"pdf_{i}")

            num_dims = st.number_input(f"כמה מידות קריטיות לבדוק עבור {part_name}?", min_value=0, step=1, key=f"num_dims_{i}")
            dims = []
            for j in range(int(num_dims)):
                st.markdown(f"📏 מידה #{j+1}")
                dim_value = st.text_input("מידה נומינלית", key=f"dim_val_{i}_{j}")
                tolerance = st.text_input("טולרנס (לדוג' ±0.2)", key=f"tol_{i}_{j}")
                comment = st.text_input("הערה (אם יש)", key=f"comment_{i}_{j}")
                dims.append((dim_value, tolerance, comment))

            st.markdown("---")
            st.markdown("🔎 סוגי בדיקות נוספות לחלק זה:")
            functional_check = st.checkbox("בדיקה פונקציונלית", key=f"func_{i}")
            go_nogo_check = st.checkbox("בדיקת Go/No-Go", key=f"gonogo_{i}")

# 🟥 טאב 3 – בקרת איכות QA
with tab3:
    st.header("🧪 בקרת איכות - QA")
    st.markdown("בחר כמה חלקים לבדוק לפי כמות הייצור (לפי תקן L2):")

    # טבלת תבחינים לפי כמות
    sampling_table = {
        (2, 8): 2,
        (9, 15): 3,
        (16, 25): 5,
        (26, 50): 8
    }

    for i, (part_name, quantity) in enumerate(st.session_state.parts_data):
        with st.expander(f"QA עבור חלק: {part_name}"):
            # קביעת מספר דגימות לפי הטבלה
            sample_size = 1
            for (min_q, max_q), sample in sampling_table.items():
                if min_q <= quantity <= max_q:
                    sample_size = sample
                    break

            st.markdown(f"🔍 יש לבדוק {sample_size} חלקים מתוך {quantity}")

            for s in range(sample_size):
                st.markdown(f"🔬 דגימה #{s+1}")
                passed = st.checkbox("✅ תקין", key=f"pass_{i}_{s}")
                note = st.text_input("הערה", key=f"note_{i}_{s}")
                go_nogo = st.checkbox("בדיקת Go/No-Go", key=f"qa_gonogo_{i}_{s}")
                functional = st.checkbox("בדיקה פונקציונלית", key=f"qa_func_{i}_{s}")
                st.markdown("---")
# ✅ טאב סיום והנפקה עם יצירת PDF ושליחה למייל
import streamlit as st
from fpdf import FPDF
import smtplib
from email.message import EmailMessage

# 📤 פונקציית שליחת מייל

def send_email_with_pdf(receiver_email, pdf_file_path):
    sender_email = "yonni@impactlabs.tech"
    app_password = "smsirhfycitcltxv"

    msg = EmailMessage()
    msg["Subject"] = "תג שמיש - חלקים שהוזנו"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg.set_content("מצורף תג השמיש בקובץ PDF.")

    with open(pdf_file_path, "rb") as f:
        pdf_data = f.read()
        msg.add_attachment(pdf_data, maintype="application", subtype="pdf", filename="tag_sheet.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

# 📄 פונקציית יצירת PDF פשוט לדוגמה

def generate_pdf(parts_data):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="תג שמיש - חלקים", ln=True, align='C')
    pdf.ln(10)

    for part_name, quantity in parts_data:
        pdf.cell(200, 10, txt=f"חלק: {part_name} | כמות: {quantity}", ln=True)

    pdf.output("tag_sheet.pdf")

# 📌 טאב אחרון באפליקציה

tab1, tab2, tab3, tab4 = st.tabs(["📦 הזנת אצווה", "📐 שרטוטים", "✅ QA", "📤 סיום והנפקה"])

with tab4:
    st.header("📤 סיום והנפקה")

    st.markdown("הפק PDF ושלח למייל שלך")
    receiver = st.text_input("כתובת מייל למשלוח", value="yonni@impactlabs.tech")

    if st.button("📄 הפק PDF ושלח למייל"):
        # דוגמה לדאטה – צריך לחבר את זה לדאטה האמיתית שלך
        parts_data = [("חלק 1", 10), ("חלק 2", 5)]

        generate_pdf(parts_data)
        send_email_with_pdf(receiver, "tag_sheet.pdf")
        st.success("✅ PDF הופק ונשלח למייל")


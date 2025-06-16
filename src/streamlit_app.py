import streamlit as st

st.set_page_config(page_title="תג שמיש - MJF", layout="wide")

# טאב ראשון - פרטי אצווה
tab1, = st.tabs(["📦 הזנת אצווה"])

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

    parts_data = []
    for i in range(int(num_parts)):
        with st.expander(f"חלק {i+1}"):
            part_name = st.text_input(f"שם חלק #{i+1}", key=f"name_{i}")
            quantity = st.number_input(f"כמות חלקים מסוג זה", min_value=1, step=1, key=f"qty_{i}")
            parts_data.append((part_name, quantity))

    st.success("בסיום שלב זה, עבור לטאב הבא להזנת שרטוט ומידות ✏️ (נוסיף בהמשך)")
tab1, tab2 = st.tabs(["📦 הזנת אצווה", "📐 שרטוטים ומידות"])

with tab2:
    st.header("📐 הזנת שרטוטים ומידות קריטיות")

    for i, (part_name, quantity) in enumerate(parts_data):
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

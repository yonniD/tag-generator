import streamlit as st
from fpdf import FPDF
from pathlib import Path

st.set_page_config(page_title="Tag Generator", layout="wide")

if "current_tab" not in st.session_state:
    st.session_state.current_tab = "Step 1"

tabs = st.tabs(["Step 1 - Batch Info", "Step 2 - Drawing & QA", "Step 3 - Generate Tag"])

# Step 1
with tabs[0]:
    st.header("Step 1 - Batch Info")
    st.text_input("Batch number", key="batch_number")
    st.text_input("Project name", key="project_name")
    st.text_input("Customer name", key="customer_name")

    if st.button("Go to Step 2"):
        st.session_state.current_tab = "Step 2"

# Step 2
with tabs[1]:
    st.header("Step 2 - Drawings and QA")

    with st.expander("Upload PDF drawing"):
        uploaded_pdf = st.file_uploader("Upload PDF", type=["pdf"])
        num_criteria = st.number_input("Number of QA checks", min_value=0, step=1)

        st.checkbox("Functional check", key="functional_check")
        st.checkbox("Go / No-Go check", key="go_nogo_check")
        st.text_area("General comments", key="qa_description")

    if st.button("Go to Step 3"):
        st.session_state.current_tab = "Step 3"

# Step 3
with tabs[2]:
    st.header("Step 3 - Generate Tag")

    if st.button("Generate PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.cell(200, 10, txt="Usable Tag - Impact Labs", ln=True, align="C")
        pdf.cell(200, 10, txt=f"Batch: {st.session_state.get('batch_number', '')}", ln=True)
        pdf.cell(200, 10, txt=f"Project: {st.session_state.get('project_name', '')}", ln=True)
        pdf.cell(200, 10, txt=f"Customer: {st.session_state.get('customer_name', '')}", ln=True)

        output_path = "tag.pdf"
        pdf.output(output_path)

        st.success("Tag generated successfully!")
        with open(output_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="tag.pdf")

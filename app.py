# app.py
import streamlit as st
from parsing import extract_text_from_pdf
from resume_chain import analyze_resume
from config import TARGET_ROLE

st.set_page_config(page_title="LLM Resume Analyzer", page_icon="📄")

st.title("📄 LLM‑Powered Resume Analyzer")
st.write("Upload your resume and get AI‑generated feedback tailored to a specific role.")

# Let user choose or override target role
target_role = st.text_input("Target Role", value=TARGET_ROLE)

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully.")
    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume using a Hugging Face + LangChain pipeline..."):
            resume_text = extract_text_from_pdf(uploaded_file)
            if not resume_text.strip():
                st.error("Could not extract text from the PDF. Try another file.")
            else:
                feedback = analyze_resume(resume_text, target_role)
                st.subheader("Analysis Result")
                st.markdown(feedback)

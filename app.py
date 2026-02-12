# app.py

import streamlit as st
from parsing import extract_text_from_pdf
from resume_chain import analyze_resume, match_resume_to_job
from config import TARGET_ROLE
from pdf_generator import create_pdf_report



st.set_page_config(page_title="Groq Resume Analyzer", page_icon="📄")

st.title("📄 LLaMA‑3 Powered Resume Analyzer (Groq API)")
st.write("Upload your resume and get a fast, high‑quality AI evaluation.")

target_role = st.text_input("Target Role", value=TARGET_ROLE)
job_description = st.text_area("Paste Job Description (Optional)")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

if uploaded_file is not None:
    st.success("Resume uploaded successfully.")



    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume using Groq LLaMA‑3..."):
            resume_text = extract_text_from_pdf(uploaded_file)

            if not resume_text.strip():
                st.error("Could not extract text from the PDF.")
            else:
                feedback = analyze_resume(resume_text, target_role)
                st.subheader("Analysis Result")
                st.markdown(feedback)
                if job_description.strip():
                    st.subheader("Job Match Analysis")
                    match_report = match_resume_to_job(resume_text, job_description)
                    st.markdown(match_report)

                pdf_bytes = create_pdf_report(feedback)

                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name="resume_analysis_report.pdf",
                    mime="application/pdf"
                )
                


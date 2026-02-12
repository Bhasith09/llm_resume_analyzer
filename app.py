# app.py

import streamlit as st
from parsing import extract_text_from_pdf
from resume_chain import (
    analyze_resume,
    match_resume_to_job,
    generate_cover_letter,
    ats_score_analysis,
)
from config import TARGET_ROLE
from pdf_generator import create_pdf_report, create_cover_letter_docx

st.set_page_config(page_title="Groq Resume Analyzer", page_icon="📄")

# Session State
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = ""

if "feedback" not in st.session_state:
    st.session_state.feedback = ""

if "ats_report" not in st.session_state:
    st.session_state.ats_report = ""

st.title("📄 LLaMA‑3 Powered Resume Analyzer (Groq API)")
st.write("Upload your resume and get a fast, high‑quality AI evaluation.")

# User type toggle
user_type = st.radio(
    "Who are you?",
    ["Job Seeker", "Recruiter"],
    horizontal=True,
)

# Inputs
target_role = st.text_input("Target Role", value=TARGET_ROLE)
job_description = st.text_area("Paste Job Description (Optional)")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Resume Upload + Analysis
if uploaded_file is not None:
    st.success("Resume uploaded successfully.")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume using Groq LLaMA‑3..."):

            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)

            if not st.session_state.resume_text.strip():
                st.error("Could not extract text from the PDF.")
            else:
                # Resume Analysis
                st.subheader("Resume Analysis")
                st.session_state.feedback = analyze_resume(
                    st.session_state.resume_text,
                    target_role,
                )
                st.markdown(st.session_state.feedback)

                # Job Match Analysis
                if job_description.strip():
                    st.subheader("Job Match Analysis")
                    match_report = match_resume_to_job(
                        st.session_state.resume_text,
                        job_description,
                    )
                    st.markdown(match_report)

                    # ATS Score & Optimization
                    st.subheader("ATS Score & Optimization")
                    st.session_state.ats_report = ats_score_analysis(
                        st.session_state.resume_text,
                        job_description,
                    )
                    st.markdown(st.session_state.ats_report)

# Cover Letter Generator
if st.session_state.resume_text:
    if st.button("Generate Cover Letter"):
        with st.spinner("Creating your personalized cover letter..."):
            st.session_state.cover_letter = generate_cover_letter(
                st.session_state.resume_text,
                job_description,
                target_role,
            )

# Show Cover Letter
if st.session_state.cover_letter:
    st.subheader("Cover Letter")

    st.markdown(
        f"<div style='text-align: justify; line-height: 1.6;'>{st.session_state.cover_letter}</div>",
        unsafe_allow_html=True,
    )

    # Download Cover Letter as Word (.docx)
    docx_file = create_cover_letter_docx(st.session_state.cover_letter)

    st.download_button(
        label="📄 Download Cover Letter as Word (.docx)",
        data=docx_file,
        file_name="cover_letter.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

# Resume Analysis PDF Download
if st.session_state.feedback:
    pdf_bytes = create_pdf_report(
        "Resume Analysis:\n\n" + st.session_state.feedback,
    )

    st.download_button(
        label="📥 Download Resume Analysis PDF",
        data=pdf_bytes,
        file_name="resume_analysis_report.pdf",
        mime="application/pdf",
    )

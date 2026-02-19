#app.py
import streamlit as st
from parsing import extract_text_from_pdf
from resume_chain import (
    analyze_resume,
    match_resume_to_job,
    generate_cover_letter,
    ats_score_analysis,
    recruiter_resume_summary,
    compare_two_resumes,
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

st.title("📄 LLaMA‑Powered Resume Analyzer (Groq API)")
st.write("Upload your resume and get a tailored AI evaluation based on who you are.")

# User type toggle
user_type = st.radio(
    "Who are you?",
    ["Job Seeker", "Recruiter"],
    horizontal=True,
)

# Inputs
target_role = st.text_input("Target Role", value=TARGET_ROLE if user_type == "Job Seeker" else "")
job_description = st.text_area("Paste Job Description (Optional)")
uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

# Resume Upload + Analysis
if uploaded_file is not None:
    st.success("Resume uploaded successfully.")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing your resume using Groq..."):

            st.session_state.resume_text = extract_text_from_pdf(uploaded_file)

            if not st.session_state.resume_text.strip():
                st.error("Could not extract text from the PDF.")
            else:
                st.subheader("Resume Analysis")

                if user_type == "Job Seeker":
                    st.session_state.feedback = analyze_resume(
                        st.session_state.resume_text,
                        target_role,
                    )
                else:
                    st.session_state.feedback = recruiter_resume_summary(
                        st.session_state.resume_text
                    )

                st.markdown(st.session_state.feedback)

                # Job Match + ATS only for Job Seekers
                if user_type == "Job Seeker" and job_description.strip():
                    st.subheader("Job Match Analysis")
                    match_report = match_resume_to_job(
                        st.session_state.resume_text,
                        job_description,
                    )
                    st.markdown(match_report)

                    st.subheader("ATS Score & Optimization")
                    st.session_state.ats_report = ats_score_analysis(
                        st.session_state.resume_text,
                        job_description,
                    )
                    st.markdown(st.session_state.ats_report)

# Cover Letter Generator — only for Job Seekers
if user_type == "Job Seeker" and st.session_state.resume_text:
    if st.button("Generate Cover Letter"):
        with st.spinner("Creating your personalized cover letter..."):
            st.session_state.cover_letter = generate_cover_letter(
                st.session_state.resume_text,
                job_description,
                target_role,
            )

# Show Cover Letter (Job Seekers only)
if user_type == "Job Seeker" and st.session_state.cover_letter:
    st.subheader("Cover Letter")

    st.markdown(
        f"<div style='text-align: justify; line-height: 1.6;'>{st.session_state.cover_letter}</div>",
        unsafe_allow_html=True,
    )

    docx_file = create_cover_letter_docx(st.session_state.cover_letter)

    st.download_button(
        label="📄 Download Cover Letter as Word (.docx)",
        data=docx_file,
        file_name="cover_letter.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

# Resume Comparison (Recruiter Only)
if user_type == "Recruiter":
    st.subheader("Compare Two Resumes")

    uploaded_file_a = st.file_uploader("Upload Resume A (PDF)", type=["pdf"], key="resume_a")
    uploaded_file_b = st.file_uploader("Upload Resume B (PDF)", type=["pdf"], key="resume_b")

    if uploaded_file_a and uploaded_file_b:
        if st.button("Compare Resumes"):
            with st.spinner("Comparing resumes..."):
                resume_a_text = extract_text_from_pdf(uploaded_file_a)
                resume_b_text = extract_text_from_pdf(uploaded_file_b)

                comparison_result = compare_two_resumes(resume_a_text, resume_b_text)

                st.subheader("Comparison Result")
                st.markdown(comparison_result)

# Resume Analysis PDF Download (both modes)
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

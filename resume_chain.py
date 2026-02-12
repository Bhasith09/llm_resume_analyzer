# resume_chain.py

import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

# Read your EXACT variable name
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found. Check your .env file.")

# Initialize Groq client using your key
client = Groq(api_key=api_key)

# -----------------------------
# NEW MODEL NAME (IMPORTANT)
MODEL_NAME = "llama3-70b-8192"
# -----------------------------


def analyze_resume(resume_text: str, target_role: str) -> str:
    prompt = f"""
You are an expert resume reviewer. Analyze the following resume for the target role: {target_role}.

Resume:
{resume_text}

Provide:
- Overall summary
- Strengths
- Weaknesses
- Suggestions to improve
- How well it fits the target role
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message["content"]


def match_resume_to_job(resume_text: str, job_description: str) -> str:
    prompt = f"""
You are an expert hiring manager. Compare this resume to the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide:
- Match percentage (0–100)
- Key strengths vs job
- Gaps vs job
- Final verdict (short)
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message["content"]


def generate_cover_letter(resume_text: str, job_description: str, target_role: str) -> str:
    prompt = f"""
You are an expert cover letter writer.

Write a professional, concise, and tailored cover letter for the role: {target_role}.

Use the resume and job description below.

Resume:
{resume_text}

Job Description:
{job_description}

Requirements:
- 3–5 short paragraphs
- Clear structure (intro, skills, alignment, closing)
- Friendly but professional tone
- No generic fluff
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4,
    )
    return response.choices[0].message["content"]


def ats_score_analysis(resume_text: str, job_description: str) -> str:
    prompt = f"""
You are an ATS (Applicant Tracking System) scanner. Analyze the resume against the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide a structured ATS report with the following sections:

1. ATS Score (0–100)
2. Keyword Match Score (0–100)
3. Matched Keywords
4. Missing Keywords
5. Missing Technical Skills
6. Missing Soft Skills
7. Experience Gaps or Red Flags
8. ATS Optimization Suggestions (very specific and actionable)

Make the output clean, bullet‑pointed, and easy to read.
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message["content"]

# resume_chain.py

import os
from dotenv import load_dotenv
from groq import Groq

# Load .env file
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("❌ GROQ_API_KEY not found in .env file.")

client = Groq(api_key=api_key)

# NEW WORKING MODEL
MODEL_NAME = "openai/gpt-oss-safeguard-20b"


def analyze_resume(resume_text: str, target_role: str) -> str:
    prompt = f"""
You are an expert resume reviewer helping a job seeker. Analyze the following resume for the target role: {target_role}.

Resume:
{resume_text}

Provide:
1. Overall summary
2. Strengths
3. Weaknesses
4. Very specific improvement suggestions
5. How well it fits the target role
6. Practical tips to make this resume more attractive to recruiters and ATS
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    return response.choices[0].message.content


def recruiter_resume_summary(resume_text: str) -> str:
    prompt = f"""
You are an expert technical recruiter. Analyze the resume and provide ONLY the following:

1. Short summary of candidate background
2. Key technical skills
3. Key soft skills
4. Relevant experience (roles, domains, industries)
5. Notable achievements
6. Overall candidate profile (1–2 lines)

Do NOT include:
- Suggestions or improvements
- ATS optimization advice
- Cover letter style content

Resume:
{resume_text}
"""
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content


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
    return response.choices[0].message.content


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
    return response.choices[0].message.content


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
    return response.choices[0].message.content

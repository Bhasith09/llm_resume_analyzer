# resume_chain.py

from groq import Groq
from config import GROQ_API_KEY, GROQ_MODEL, TARGET_ROLE

client = Groq(api_key=GROQ_API_KEY)

PROMPT_TEMPLATE = """
You are an expert technical recruiter specializing in {target_role} roles.

Your task is to evaluate the resume below and produce a structured, detailed, and ORIGINAL analysis.

RULES:
- Do NOT repeat the resume text.
- Do NOT repeat the instructions.
- Keep each section concise but insightful.
- Use bullet points where appropriate.
- Make the output clean and well formatted.

RESUME:
{resume_text}

Now produce the following sections EXACTLY in this order:

### 1. Candidate Summary (3–4 lines)

### 2. Score for {target_role} (1–10) + Justification

### 3. Key Strengths (4–6 bullet points)

### 4. Key Weaknesses / Gaps (3–5 bullet points)

### 5. Actionable Suggestions (5 items)
"""

def analyze_resume(resume_text: str, target_role: str = TARGET_ROLE) -> str:
    prompt = PROMPT_TEMPLATE.format(
        resume_text=resume_text,
        target_role=target_role
    )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": "You are an expert resume evaluator."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=800,
    )

    return response.choices[0].message.content

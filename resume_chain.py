# resume_chain.py
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.llms import HuggingFacePipeline

from config import HF_MODEL_NAME, TARGET_ROLE

# 1. Load HF model + tokenizer
tokenizer = AutoTokenizer.from_pretrained(HF_MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(HF_MODEL_NAME)

# 2. Create a transformers pipeline
hf_pipe = pipeline(
    "text2text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    temperature=0.3,
)

# 3. Wrap it with LangChain's HuggingFacePipeline
llm = HuggingFacePipeline(pipeline=hf_pipe)

# 4. Define the prompt template
prompt_template = """
You are an expert technical recruiter for {target_role} roles.

Analyze the following resume and provide a detailed evaluation.

RESUME:
\"\"\" 
{resume_text}
\"\"\"

Please respond in the following structured format:

1. Candidate Summary (3-4 lines)
2. Score for the role of {target_role} (1-10) with a short justification
3. Key Strengths (bullet points)
4. Key Weaknesses / Gaps (bullet points)
5. 5 Specific, Actionable Suggestions to Improve the Resume for a {target_role} role

Make the response clear and well formatted.
"""

prompt = PromptTemplate(
    input_variables=["resume_text", "target_role"],
    template=prompt_template,
)

# 5. Create the LLMChain
resume_chain = LLMChain(
    llm=llm,
    prompt=prompt,
)

def analyze_resume(resume_text: str, target_role: str = TARGET_ROLE) -> str:
    """
    Run the LangChain LLMChain on the given resume text and target role.
    """
    result = resume_chain.invoke({
        "resume_text": resume_text,
        "target_role": target_role,
    })
    # LLMChain returns a dict with 'text' key
    return result["text"]

# config.py
import os
from dotenv import load_dotenv
load_dotenv()
TARGET_ROLE = "Machine Learning Engineer"

# Groq model name
GROQ_MODEL = "llama-3.1-8b-instant"


# Add your API key here (or load from environment variable)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

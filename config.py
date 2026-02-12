# config.py

import os
from dotenv import load_dotenv

load_dotenv()

TARGET_ROLE = "Machine Learning Engineer"

# Updated Groq model name
GROQ_MODEL = "llama-3.1-8b-instant"

# Load API key from .env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

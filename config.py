import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set OPENAI_API_KEY in a .env file")

# Ensure the new OpenAI SDK can read the key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

MODEL_NAME = "gpt-4o-mini"  # or "gpt-4o"
MAX_TOKENS = 4000
TEMPERATURE = 0.1

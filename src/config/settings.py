import os

from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def is_groq_configured() -> bool:
    return bool(GROQ_API_KEY)
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY        = os.getenv("GROQ_API_KEY")
SERVICE_AUTH_TOKEN  = os.getenv("SERVICE_AUTH_TOKEN")

# Switched from llama-3.3-70b-versatile — that model is too "helpful"
# and ignores formatting instructions, defaulting to long generic responses.
# llama-3.1-8b-instant follows system prompt rules much more strictly.
MODEL_NAME = "llama-3.1-8b-instant"
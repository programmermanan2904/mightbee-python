from pydantic import BaseModel
from typing import List, Optional


# ============================================================
# A single message in the conversation history
# ============================================================

class ChatMessage(BaseModel):
    role: str        # "user" or "assistant"
    content: str     # the actual message text


# ============================================================
# User Understanding Engine profile
# Built by Node.js from MongoDB and sent with each request
# ============================================================

class UserProfile(BaseModel):
    interests: Optional[List[str]] = []           # e.g. ["gaming", "horror movies"]
    lifestyle: Optional[str] = None               # e.g. "student", "working professional"
    financial_preference: Optional[str] = None    # e.g. "budget conscious", "premium"
    personality: Optional[str] = None             # e.g. "analytical", "casual"


# ============================================================
# Request payload Node.js sends to Python
# ============================================================

class ChatRequest(BaseModel):

    # current user message
    message: str

    # conversation memory from MongoDB
    chat_history: List[ChatMessage]

    # optional user context
    user_profile: Optional[UserProfile] = None

    # tone selected in frontend
    # if None → Livvy auto-detects tone
    tone: Optional[str] = None


# ============================================================
# Response returned to Node.js
# ============================================================

class ChatResponse(BaseModel):
    reply: str
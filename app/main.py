from fastapi import FastAPI, HTTPException, Header
from app.models import ChatRequest, ChatResponse
from app.livvy import get_livvy_response
from app.config import SERVICE_AUTH_TOKEN


app = FastAPI(
    title="Livvy AI Microservice",
    description="The dedicated AI service powering Livvy, MightBee's context-aware companion",
    version="2.0.0"
)


# ============================================================
# Health Check
# ============================================================

@app.get("/")
def health_check():
    """Confirms the service is live."""
    return {
        "status": "Livvy is online 🐝",
        "version": "2.0.0"
    }


# ============================================================
# Main Chat Endpoint
# Called ONLY by the Node.js backend
# ============================================================

@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    authorization: str = Header(None)
):

    """
    Node.js sends a request like:

    {
        "message": "what should I watch tonight?",
        "chat_history": [
            { "role": "user", "content": "I'm tired from studying" },
            { "role": "assistant", "content": "That sounds exhausting..." }
        ],
        "user_profile": {
            "interests": ["horror movies", "gaming"],
            "lifestyle": "student",
            "financial_preference": "budget conscious",
            "personality": "casual"
        },
        "tone": "witty"
    }

    tone can also be null → Livvy auto-detects tone.
    """


    # ============================================================
    # SECURITY CHECK
    # Only allow calls from Node.js backend
    # ============================================================

    expected_token = f"Bearer {SERVICE_AUTH_TOKEN}"

    if authorization != expected_token:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized — invalid service token"
        )


    # ============================================================
    # CALL LIVVY INTELLIGENCE PIPELINE
    # ============================================================

    try:

        reply = get_livvy_response(
            message=request.message,
            chat_history=request.chat_history,
            user_profile=request.user_profile,
            tone=request.tone     # ← tone forwarded here
        )

        return ChatResponse(reply=reply)


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Livvy encountered an error: {str(e)}"
        )
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

load_dotenv()

from models import WebhookResponse, IncomingMessage
from services.normalizer import normalize
from services.classifier import classify
from services.claude_handler import claude_reply
from services.confidence import calculate_confidence

app = FastAPI(title="Nistula Message Handler")

@app.post("/webhook/message", response_model=WebhookResponse)
async def handle_message(payload: IncomingMessage):
    try:
        normalized = normalize(payload)
        normalized.query_type = classify(normalized.message_text)
        reply = claude_reply(normalized)
        score, action = calculate_confidence(normalized.query_type, reply, normalized.message_text)
        
        return WebhookResponse(
                            message_id=normalized.message_id, 
                            query_type=normalized.query_type,
                            drafted_reply=reply,
                            confidence_score=score,
                            action=action
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
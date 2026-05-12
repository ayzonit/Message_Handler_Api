from pydantic import BaseModel
from typing import Optional


class IncomingMessage(BaseModel):
    source: str
    guest_name: str
    message: str
    timestamp: str
    booking_ref: Optional[str] = None
    property_id: Optional[str] = None
    
    
class NormalizedMessage(BaseModel):
    message_id: str
    source: str
    guest_name: str
    message_text: str
    timestamp: str
    booking_ref: Optional[str] = None
    property_id: Optional[str] = None
    query_type: Optional[str] = None
    

class WebhookResponse(BaseModel):
    message_id: str
    query_type: str
    drafted_reply: str
    confidence_score: float
    action: str
import uuid
from app.models import IncomingMessage, NormalizedMessage

def normalize(payload: IncomingMessage) -> NormalizedMessage:
    return NormalizedMessage(
        message_id = str(uuid.uuid4()),
        source = payload.source,
        guest_name = payload.guest_name,
        message_text = payload.message,
        timestamp = payload.timestamp,
        booking_ref = payload.booking_ref,
        property_id = payload.property_id,
        query_type = None
    )
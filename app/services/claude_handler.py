import os 
from anthropic import Anthropic
from app.property_context import PROPERTY_CONTEXT
from app.models import NormalizedMessage

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def claude_reply(normalized_msg: NormalizedMessage) -> str:
    prompt = f"""You are a calm and professional hospitality assistant for Nistula Villas.
    
PROPERTY_CONTEXT: {PROPERTY_CONTEXT}

GUEST DETAILS:
Name: {normalized_msg.guest_name}
Booking Ref: {normalized_msg.booking_ref or 'N/A'}
Source: {normalized_msg.source}
Query Type: {normalized_msg.query_type}

GUEST MESSAGE:
{normalized_msg.message_text}

Instructions:
- Address the guest by his first name.
- Reply warmly and concisely.
- Use only the property context above, never make up details.
- If something is not in the context, say that you will check and get back to them.
- Keep it under 100 words"""

    response = client.messages.create(model="claude-sonnet-4-20250514",
                                      max_tokens=200,
                                      messages=[{"role": "user", "content": prompt}])
    return response.content[0].text.strip()
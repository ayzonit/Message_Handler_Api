import os
from anthropic import Anthropic

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

QUERY_TYPES = [
    "pre_sales_availability",
    "pre_sales_pricing",
    "post_sales_checkin",
    "special_request",
    "complaint",
    "general_enquiry"
]

def classify(message_text: str) -> str:
    prompt = f"""Classify this guest message into exactly one of these types:
{', '.join(QUERY_TYPES)}
    
Message: "{message_text}"
Reply with type label only, nothing else"""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{"role": "user", "content": prompt}]
    )
    
    result = response.content[0].text.strip().lower()
    return result if result in QUERY_TYPES else "general_enquiry"
import re


VAGUE_PHRASES = [
    "will check",
    "get back to you",
    "get back to them",
    "not sure",
    "cannot confirm",
    "can't confirm",
    "unable to confirm",
    "please note"]

QUERY_KEYWORDS = {
    "pre_sales_availability": {"available", "availability", "dates", "date", "vacancy", "book"},
    "pre_sales_pricing": {"rate", "price", "pricing", "cost", "inr", "night", "nights", "guest"},
    "post_sales_checkin": {"checkin", "wifi", "password", "arrival", "keys"},
    "special_request": {"arrange", "transfer", "early", "late", "request", "chef", "pickup"},
    "complaint": {"issue", "problem", "sorry", "apologize", "apology"},
    "general_enquiry": {"pets", "parking", "policy", "allow", "amenities"}
}

def tokenize(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9']+", text.lower()))

def calculate_confidence(query_type: str, reply: str, message_text: str) -> tuple[float, str]:
    if query_type == "complaint":
        return 0.40, "escalate"
    
    reply_clean = reply.strip().lower()
    if not reply_clean:
        return 0.0, "escalate"
    
    score = 0.55
    word_count = len(reply_clean.split())
    if word_count < 12:
        score -= 0.12
    elif word_count > 100:
        score -= 0.08
    else:
        score += 0.05

    if any(phrase in reply_clean for phrase in VAGUE_PHRASES):
        score -= 0.15

    reply_tokens = tokenize(reply)
    message_tokens = tokenize(message_text)
    
    query_keywords = QUERY_KEYWORDS.get(query_type, set())
    keyword_hits = len(query_keywords & reply_tokens)
    if keyword_hits >= 2:
        score += 0.14
    elif keyword_hits == 1:
        score += 0.08
    else:
        score -= 0.08
            
    content_overlap = len((message_tokens & reply_tokens) - {"the", "and", "is", "are", "to", "for", "of"})
    if content_overlap >= 3:
        score += 0.08
    elif content_overlap == 0:
        score -= 0.10
        
    if query_type == "pre_sales_availability":
        if "available" in reply_tokens:
            score += 0.08
        if any(char.isdigit() for char in reply_clean):
            score += 0.04

    elif query_type == "pre_sales_pricing":
        if any(term in reply_tokens for term in {"inr", "rate", "price", "cost", "night"}):
            score += 0.10

    elif query_type == "post_sales_checkin":
        if any(term in reply_tokens for term in {"checkin", "wifi", "password"}):
            score += 0.10

    elif query_type == "special_request":
        if any(term in reply_tokens for term in {"arrange", "request", "transfer", "chef", "pickup"}):
            score += 0.08

    elif query_type == "general_enquiry":
        if any(term in reply_tokens for term in {"allow", "parking", "pets", "yes"}):
            score += 0.06
            
    score = round(min(max(score, 0.0), 1.0), 2)
    
    if score < 0.60:
        action = "escalate"
    elif 0.60 <= score <= 0.85:
        action = "agent_review"
    else:
        action = "auto_send"
        
    return score, action

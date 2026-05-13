
-- Needed for UUID generation
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- One row per real guest, regardless of channel
CREATE TABLE guests (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Maps a guest to external channel identities
CREATE TABLE channel_identities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID NOT NULL REFERENCES guests(id) ON DELETE CASCADE,
    channel VARCHAR(50) NOT NULL,
    channel_guest_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (channel, channel_guest_id),
    CHECK (channel IN ('whatsapp', 'booking_com', 'airbnb', 'instagram', 'direct'))
);

-- Reservation records linked to guests
CREATE TABLE reservations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    booking_ref VARCHAR(100) UNIQUE NOT NULL,
    guest_id UUID NOT NULL REFERENCES guests(id) ON DELETE CASCADE,
    property_id VARCHAR(100) NOT NULL,
    check_in DATE,
    check_out DATE,
    num_guests INTEGER,
    status VARCHAR(50) NOT NULL DEFAULT 'confirmed',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (status IN ('confirmed', 'cancelled', 'completed', 'pending'))
);

-- Conversation thread linked to guest and optional reservation
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    guest_id UUID NOT NULL REFERENCES guests(id) ON DELETE CASCADE,
    reservation_id UUID REFERENCES reservations(id) ON DELETE SET NULL,
    channel VARCHAR(50) NOT NULL,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message_at TIMESTAMPTZ,
    CHECK (channel IN ('whatsapp', 'booking_com', 'airbnb', 'instagram', 'direct'))
);

-- All Incoming and Outgoing messages in one table
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    direction VARCHAR(10) NOT NULL,
    source VARCHAR(50) NOT NULL,
    message_text TEXT NOT NULL,
    sent_at TIMESTAMPTZ NOT NULL,
    query_type VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (direction IN ('incoming', 'outgoing')),
    CHECK (source IN ('whatsapp', 'booking_com', 'airbnb', 'instagram', 'direct')),
    CHECK (
        query_type IS NULL OR query_type IN (
            'pre_sales_availability',
            'pre_sales_pricing',
            'post_sales_checkin',
            'special_request',
            'complaint',
            'general_enquiry'
        )
    )
);

-- AI processing record for each inbound message
CREATE TABLE ai_message_decisions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL UNIQUE REFERENCES messages(id) ON DELETE CASCADE,
    drafted_reply TEXT NOT NULL,
    confidence_score NUMERIC(4,3) NOT NULL CHECK (confidence_score >= 0 AND confidence_score <= 1),
    action VARCHAR(20) NOT NULL,
    outcome VARCHAR(20) NOT NULL,
    agent_reply TEXT,
    resolved_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (action IN ('auto_send', 'agent_review', 'escalate')),
    CHECK (outcome IN ('ai_drafted', 'agent_edited', 'auto_sent', 'escalated', 'discarded'))
);

-- Helpful indexes
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_sent_at ON messages(sent_at);
CREATE INDEX idx_ai_message_decisions_message_id ON ai_message_decisions(message_id);
CREATE INDEX idx_conversations_guest_id ON conversations(guest_id);


-- Hardest design decision--
-- One of the hard design decisions was deciding how to represent guests across multiple platforms. 
-- A single guest could contact the system through WhatsApp, Airbnb, Booking.com, or Instagram with different identifiers. 
-- Instead of storing different IDs for different platforms in the 'guests' table, I created a separate 'channel_identities' table. 
-- This keeps the database clean while one guest can still be linked to multiple external platforms and accounts.
-- Supabase Database Schema for Aushadham
-- Run this SQL in your Supabase SQL Editor to create the necessary tables

-- Enable UUID extension if not already enabled
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    username VARCHAR(80) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(120),
    phone VARCHAR(20),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Saved questionnaires table
CREATE TABLE IF NOT EXISTS saved_questionnaires (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    symptom VARCHAR(200) NOT NULL,
    initial_description TEXT,
    answers JSONB NOT NULL,
    report JSONB,
    severity VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for saved_questionnaires
CREATE INDEX IF NOT EXISTS idx_saved_questionnaires_user_id ON saved_questionnaires(user_id);
CREATE INDEX IF NOT EXISTS idx_saved_questionnaires_session_id ON saved_questionnaires(session_id);
CREATE INDEX IF NOT EXISTS idx_saved_questionnaires_created_at ON saved_questionnaires(created_at DESC);

-- User feedback table
CREATE TABLE IF NOT EXISTS user_feedback (
    id BIGSERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    questionnaire_id BIGINT REFERENCES saved_questionnaires(id) ON DELETE SET NULL,
    rating INTEGER CHECK (rating >= 1 AND rating <= 5),
    comment TEXT,
    feedback_type VARCHAR(50),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for user_feedback
CREATE INDEX IF NOT EXISTS idx_user_feedback_user_id ON user_feedback(user_id);
CREATE INDEX IF NOT EXISTS idx_user_feedback_questionnaire_id ON user_feedback(questionnaire_id);
CREATE INDEX IF NOT EXISTS idx_user_feedback_created_at ON user_feedback(created_at DESC);

-- Enable Row Level Security (RLS)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE saved_questionnaires ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_feedback ENABLE ROW LEVEL SECURITY;

-- RLS Policies for users table
-- Users can read their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT
    USING (true);

-- Users can update their own data
CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE
    USING (true);

-- Allow inserts (for registration)
CREATE POLICY "Allow user registration" ON users
    FOR INSERT
    WITH CHECK (true);

-- RLS Policies for saved_questionnaires table
-- Users can only see their own questionnaires
CREATE POLICY "Users can view own questionnaires" ON saved_questionnaires
    FOR SELECT
    USING (true);

-- Users can insert their own questionnaires
CREATE POLICY "Users can create questionnaires" ON saved_questionnaires
    FOR INSERT
    WITH CHECK (true);

-- Users can delete their own questionnaires
CREATE POLICY "Users can delete own questionnaires" ON saved_questionnaires
    FOR DELETE
    USING (true);

-- RLS Policies for user_feedback table
-- Users can view their own feedback
CREATE POLICY "Users can view own feedback" ON user_feedback
    FOR SELECT
    USING (true);

-- Users can insert their own feedback
CREATE POLICY "Users can create feedback" ON user_feedback
    FOR INSERT
    WITH CHECK (true);

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL TABLES IN SCHEMA public TO anon, authenticated;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO anon, authenticated;

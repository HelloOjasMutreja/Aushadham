# Aushadham API Documentation

## Overview

Aushadham is a medical questionnaire API with user authentication that allows users to:
- Register and login with secure JWT authentication
- Complete medical questionnaires
- Save questionnaire results to their profile
- Provide feedback on questionnaires

**Base URL:** `http://localhost:5000`

**Version:** 4.1

## Database Backend

The API supports two database backends:
- **Supabase** (recommended for production) - Cloud PostgreSQL with real-time capabilities
- **SQLAlchemy** - Local SQLite/PostgreSQL/MySQL

The API behavior is identical regardless of which backend is used. See [SUPABASE_SETUP.md](SUPABASE_SETUP.md) for setup instructions.

## Authentication

Most endpoints require authentication using JWT (JSON Web Tokens). After registration or login, you'll receive an `access_token` that must be included in the `Authorization` header:

```
Authorization: Bearer <your_access_token>
```

## Endpoints

### Authentication Endpoints

#### 1. Register User

**POST** `/register`

Register a new user account.

**Request Body:**
```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password",
  "full_name": "John Doe",
  "phone": "1234567890"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "1234567890",
    "created_at": "2025-11-04T08:21:24.588357"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 2. Login

**POST** `/login`

Login with username (or email) and password.

**Request Body:**
```json
{
  "username": "john_doe",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "1234567890",
    "created_at": "2025-11-04T08:21:24.588357"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

#### 3. Get Profile

**GET** `/profile` 🔒 *Requires Authentication*

Get the current user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "phone": "1234567890",
    "created_at": "2025-11-04T08:21:24.588357"
  }
}
```

#### 4. Update Profile

**PUT** `/profile` 🔒 *Requires Authentication*

Update the current user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "full_name": "John Smith",
  "phone": "9876543210",
  "email": "john.smith@example.com"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Profile updated successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john.smith@example.com",
    "full_name": "John Smith",
    "phone": "9876543210",
    "created_at": "2025-11-04T08:21:24.588357"
  }
}
```

### Questionnaire Endpoints

#### 5. Start Questionnaire

**POST** `/start_questionnaire`

Start a new medical questionnaire session.

**Request Body:**
```json
{
  "symptom": "stomach pain",
  "description": "I have severe stomach pain"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb",
  "message": "Starting questionnaire for: stomach pain",
  "question": {
    "question": "Did you drink enough water today (at least 6-8 glasses)?",
    "type": "yes_no",
    "options": ["Yes", "No"],
    "current": 1,
    "total": 12,
    "progress": 8.33
  }
}
```

#### 6. Submit Answer

**POST** `/submit_answer`

Submit an answer and navigate through the questionnaire.

**Request Body:**
```json
{
  "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb",
  "answer": "Yes",
  "action": "next"
}
```

**Actions:** `next`, `previous`, `skip`

**Response (200 OK):**
```json
{
  "success": true,
  "completed": false,
  "question": {
    "question": "Next question...",
    "type": "yes_no",
    "options": ["Yes", "No"],
    "current": 2,
    "total": 12,
    "progress": 16.67
  }
}
```

#### 7. Get Current Question

**POST** `/get_current_question`

Get the current question in the questionnaire.

**Request Body:**
```json
{
  "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb"
}
```

#### 8. Get Report

**POST** `/get_report`

Generate a comprehensive medical report based on answers.

**Request Body:**
```json
{
  "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "report": {
    "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb",
    "symptom": "stomach pain",
    "severity": "Moderate",
    "urgency": "Consult a doctor within 24 hours",
    "risk_score": 12,
    "recommendations": [
      "Stay hydrated with small sips of water",
      "Eat bland foods (BRAT diet: Bananas, Rice, Applesauce, Toast)",
      "Avoid dairy, caffeine, and fatty foods"
    ],
    "suggested_medications": [
      {
        "name": "Antacids (Tums, Mylanta)",
        "purpose": "For acid reflux or indigestion"
      }
    ],
    "disclaimer": "This assessment is for informational purposes only..."
  }
}
```

#### 9. Save Questionnaire

**POST** `/save_questionnaire` 🔒 *Requires Authentication*

Save a completed questionnaire to the user's profile.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Questionnaire saved successfully",
  "questionnaire": {
    "id": 1,
    "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb",
    "symptom": "stomach pain",
    "severity": "Moderate",
    "created_at": "2025-11-04T08:21:57.842533",
    "answers": {...},
    "report": {...}
  }
}
```

#### 10. Get My Questionnaires

**GET** `/my_questionnaires` 🔒 *Requires Authentication*

Get all saved questionnaires for the current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "questionnaires": [
    {
      "id": 2,
      "symptom": "headache",
      "severity": "Low",
      "created_at": "2025-11-04T09:30:00.000000"
    },
    {
      "id": 1,
      "symptom": "stomach pain",
      "severity": "Moderate",
      "created_at": "2025-11-04T08:21:57.842533"
    }
  ]
}
```

#### 11. Get Questionnaire Details

**GET** `/my_questionnaires/<id>` 🔒 *Requires Authentication*

Get detailed information about a specific saved questionnaire.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "questionnaire": {
    "id": 1,
    "session_id": "67f44b50-409a-478b-bd1f-b081e78a01bb",
    "symptom": "stomach pain",
    "severity": "Moderate",
    "answers": {...},
    "report": {...},
    "created_at": "2025-11-04T08:21:57.842533"
  }
}
```

#### 12. Delete Questionnaire

**DELETE** `/my_questionnaires/<id>` 🔒 *Requires Authentication*

Delete a saved questionnaire.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Questionnaire deleted successfully"
}
```

### Feedback Endpoints

#### 13. Submit Feedback

**POST** `/feedback` 🔒 *Requires Authentication*

Submit feedback about a questionnaire or general feedback.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Request Body:**
```json
{
  "questionnaire_id": 1,
  "rating": 5,
  "comment": "Very helpful assessment!",
  "feedback_type": "questionnaire"
}
```

**Feedback Types:** `general`, `questionnaire`, `recommendation`

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Feedback submitted successfully",
  "feedback": {
    "id": 1,
    "questionnaire_id": 1,
    "rating": 5,
    "comment": "Very helpful assessment!",
    "feedback_type": "questionnaire",
    "created_at": "2025-11-04T08:22:10.407792"
  }
}
```

#### 14. Get My Feedback

**GET** `/my_feedback` 🔒 *Requires Authentication*

Get all feedback submitted by the current user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "success": true,
  "count": 2,
  "feedback": [
    {
      "id": 2,
      "questionnaire_id": 2,
      "rating": 4,
      "comment": "Good assessment",
      "feedback_type": "questionnaire",
      "created_at": "2025-11-04T09:30:00.000000"
    },
    {
      "id": 1,
      "questionnaire_id": 1,
      "rating": 5,
      "comment": "Very helpful assessment!",
      "feedback_type": "questionnaire",
      "created_at": "2025-11-04T08:22:10.407792"
    }
  ]
}
```

### Health Check

#### 15. Health Check

**GET** `/health_check`

Check the health status of the API.

**Response (200 OK):**
```json
{
  "status": "healthy",
  "active_sessions": 3,
  "timestamp": "2025-11-04T08:22:00.000000"
}
```

## Error Responses

All endpoints may return error responses in the following format:

```json
{
  "success": false,
  "error": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `200 OK` - Request successful
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required or invalid credentials
- `404 Not Found` - Resource not found
- `409 Conflict` - Resource already exists

## Database Schema

### Users Table
- `id` (Primary Key)
- `username` (Unique)
- `email` (Unique)
- `password_hash`
- `full_name`
- `phone`
- `created_at`

### Saved Questionnaires Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `session_id` (Unique)
- `symptom`
- `initial_description`
- `answers` (JSON)
- `report` (JSON)
- `severity`
- `created_at`

### User Feedback Table
- `id` (Primary Key)
- `user_id` (Foreign Key → Users)
- `questionnaire_id` (Foreign Key → Saved Questionnaires, Optional)
- `rating` (1-5)
- `comment`
- `feedback_type`
- `created_at`

## Environment Variables

Create a `.env` file based on `.env.example`:

```bash
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///aushadham.db
```

## Running the API

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start the server:
```bash
python app.py
```

3. The API will be available at `http://localhost:5000`

## Testing

Run the test script:
```bash
python test_api.py
```

## Security Features

- Password hashing using bcrypt
- JWT-based authentication
- Token expiration (24 hours)
- Protected endpoints require authentication
- SQL injection prevention via SQLAlchemy ORM
- CORS support for cross-origin requests

## Notes

- All questionnaire sessions are temporary and stored in memory
- Only completed questionnaires can be saved to user profiles
- Users can only access their own data
- Tokens expire after 24 hours
- Database tables are created automatically on first run

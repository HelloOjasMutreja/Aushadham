#!/usr/bin/env python3
"""
Test script for Aushadham API with authentication
This script tests the API endpoints and works with both Supabase and SQLAlchemy backends.
"""
import requests
import json
import sys
import os

BASE_URL = "http://127.0.0.1:5000"

# Check which database backend is being used
USE_SUPABASE = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
print(f"Testing with {'Supabase' if USE_SUPABASE else 'SQLAlchemy'} backend\n")

def test_registration():
    """Test user registration"""
    print("\n=== Testing User Registration ===")
    response = requests.post(f"{BASE_URL}/register", json={
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpass123",
        "full_name": "Test User 2",
        "phone": "9876543210"
    })
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"User ID: {data['user']['id']}")
        print(f"Username: {data['user']['username']}")
        return data.get('access_token')
    return None

def test_login():
    """Test user login"""
    print("\n=== Testing User Login ===")
    response = requests.post(f"{BASE_URL}/login", json={
        "username": "testuser2",
        "password": "testpass123"
    })
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"Token received: {data.get('access_token')[:20]}...")
        return data.get('access_token')
    return None

def test_profile(token):
    """Test getting user profile"""
    print("\n=== Testing Get Profile ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/profile", headers=headers)
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Success: {data.get('success')}")
    if data.get('success'):
        print(f"User: {data['user']['username']} ({data['user']['email']})")

def test_questionnaire_flow(token):
    """Test questionnaire with saving"""
    print("\n=== Testing Questionnaire Flow ===")
    
    # Start questionnaire
    response = requests.post(f"{BASE_URL}/start_questionnaire", json={
        "symptom": "headache",
        "description": "Severe headache since morning"
    })
    data = response.json()
    session_id = data.get('session_id')
    print(f"Questionnaire started: {session_id}")
    
    # Answer some questions
    for i in range(3):
        response = requests.post(f"{BASE_URL}/submit_answer", json={
            "session_id": session_id,
            "answer": "Yes",
            "action": "next"
        })
    
    # Get report
    response = requests.post(f"{BASE_URL}/get_report", json={
        "session_id": session_id
    })
    report_data = response.json()
    print(f"Report generated. Severity: {report_data['report']['severity']}")
    
    # Save questionnaire
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/save_questionnaire", 
                            headers=headers,
                            json={"session_id": session_id})
    print(f"Save status: {response.status_code}")
    save_data = response.json()
    print(f"Questionnaire saved: {save_data.get('success')}")
    
    return save_data.get('questionnaire', {}).get('id')

def test_get_questionnaires(token):
    """Test getting saved questionnaires"""
    print("\n=== Testing Get Questionnaires ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/my_questionnaires", headers=headers)
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Total questionnaires: {data.get('count')}")
    if data.get('questionnaires'):
        for q in data['questionnaires']:
            print(f"  - {q['symptom']} (Severity: {q['severity']}) at {q['created_at']}")

def test_feedback(token, questionnaire_id):
    """Test submitting feedback"""
    print("\n=== Testing Feedback Submission ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/feedback", 
                            headers=headers,
                            json={
                                "questionnaire_id": questionnaire_id,
                                "rating": 4,
                                "comment": "Good assessment, very detailed",
                                "feedback_type": "questionnaire"
                            })
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Feedback ID: {data.get('feedback', {}).get('id')}")

def test_get_feedback(token):
    """Test getting feedback"""
    print("\n=== Testing Get Feedback ===")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/my_feedback", headers=headers)
    data = response.json()
    print(f"Success: {data.get('success')}")
    print(f"Total feedback: {data.get('count')}")

def main():
    """Run all tests"""
    print("Starting API Tests...")
    
    # Test registration (or use existing user)
    token = test_registration()
    if not token:
        # If registration fails (user exists), try login
        token = test_login()
    
    if not token:
        print("\nFailed to get authentication token!")
        sys.exit(1)
    
    # Test authenticated endpoints
    test_profile(token)
    questionnaire_id = test_questionnaire_flow(token)
    test_get_questionnaires(token)
    
    if questionnaire_id:
        test_feedback(token, questionnaire_id)
        test_get_feedback(token)
    
    print("\n=== All Tests Completed Successfully! ===")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print(f"Error: Could not connect to API. Make sure the server is running at {BASE_URL}")
        sys.exit(1)
    except Exception as e:
        print(f"Error during testing: {e}")
        sys.exit(1)

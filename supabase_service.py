"""
Supabase database service layer for Aushadham
Provides an abstraction layer for database operations using Supabase
"""
import os
import bcrypt
from datetime import datetime
from typing import Dict, List, Optional
from supabase import create_client, Client
import logging

logger = logging.getLogger(__name__)


class SupabaseService:
    """Service class to handle all Supabase database operations"""
    
    def __init__(self, supabase_url: str, supabase_key: str):
        """Initialize Supabase client"""
        try:
            self.client: Client = create_client(supabase_url, supabase_key)
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {e}")
            raise
    
    # User Management
    def create_user(self, username: str, email: str, password: str, 
                   full_name: str = '', phone: str = '') -> Optional[Dict]:
        """Create a new user in Supabase"""
        try:
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Insert user
            data = {
                'username': username,
                'email': email,
                'password_hash': password_hash,
                'full_name': full_name,
                'phone': phone,
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.client.table('users').insert(data).execute()
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise
    
    def get_user_by_username(self, username: str) -> Optional[Dict]:
        """Get user by username"""
        try:
            response = self.client.table('users').select('*').eq('username', username).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by username: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            response = self.client.table('users').select('*').eq('email', email).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by email: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        try:
            response = self.client.table('users').select('*').eq('id', user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting user by ID: {e}")
            return None
    
    def update_user(self, user_id: int, updates: Dict) -> Optional[Dict]:
        """Update user information"""
        try:
            response = self.client.table('users').update(updates).eq('id', user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error updating user: {e}")
            raise
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    # Questionnaire Management
    def save_questionnaire(self, user_id: int, session_id: str, symptom: str,
                          initial_description: str, answers: Dict, report: Dict,
                          severity: str) -> Optional[Dict]:
        """Save a completed questionnaire"""
        try:
            data = {
                'user_id': user_id,
                'session_id': session_id,
                'symptom': symptom,
                'initial_description': initial_description,
                'answers': answers,
                'report': report,
                'severity': severity,
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.client.table('saved_questionnaires').insert(data).execute()
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error saving questionnaire: {e}")
            raise
    
    def get_questionnaire_by_session_id(self, session_id: str) -> Optional[Dict]:
        """Get questionnaire by session ID"""
        try:
            response = self.client.table('saved_questionnaires').select('*').eq('session_id', session_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting questionnaire by session ID: {e}")
            return None
    
    def get_user_questionnaires(self, user_id: int) -> List[Dict]:
        """Get all questionnaires for a user"""
        try:
            response = self.client.table('saved_questionnaires')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Error getting user questionnaires: {e}")
            return []
    
    def get_questionnaire_by_id(self, questionnaire_id: int, user_id: int) -> Optional[Dict]:
        """Get a specific questionnaire by ID for a user"""
        try:
            response = self.client.table('saved_questionnaires')\
                .select('*')\
                .eq('id', questionnaire_id)\
                .eq('user_id', user_id)\
                .execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error getting questionnaire by ID: {e}")
            return None
    
    def delete_questionnaire(self, questionnaire_id: int, user_id: int) -> bool:
        """Delete a questionnaire"""
        try:
            response = self.client.table('saved_questionnaires')\
                .delete()\
                .eq('id', questionnaire_id)\
                .eq('user_id', user_id)\
                .execute()
            return True
        except Exception as e:
            logger.error(f"Error deleting questionnaire: {e}")
            raise
    
    # Feedback Management
    def create_feedback(self, user_id: int, questionnaire_id: Optional[int],
                       rating: Optional[int], comment: str, feedback_type: str) -> Optional[Dict]:
        """Create user feedback"""
        try:
            data = {
                'user_id': user_id,
                'questionnaire_id': questionnaire_id,
                'rating': rating,
                'comment': comment,
                'feedback_type': feedback_type,
                'created_at': datetime.utcnow().isoformat()
            }
            
            response = self.client.table('user_feedback').insert(data).execute()
            
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error creating feedback: {e}")
            raise
    
    def get_user_feedback(self, user_id: int) -> List[Dict]:
        """Get all feedback submitted by a user"""
        try:
            response = self.client.table('user_feedback')\
                .select('*')\
                .eq('user_id', user_id)\
                .order('created_at', desc=True)\
                .execute()
            return response.data if response.data else []
        except Exception as e:
            logger.error(f"Error getting user feedback: {e}")
            return []


def get_supabase_service() -> Optional[SupabaseService]:
    """Factory function to create SupabaseService instance"""
    supabase_url = os.getenv('SUPABASE_URL')
    supabase_key = os.getenv('SUPABASE_KEY')
    
    if not supabase_url or not supabase_key:
        logger.warning("Supabase credentials not found in environment")
        return None
    
    try:
        return SupabaseService(supabase_url, supabase_key)
    except Exception as e:
        logger.error(f"Failed to create Supabase service: {e}")
        return None

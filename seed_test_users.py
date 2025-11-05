"""
Script to seed test user accounts for easier testing
"""
from app import app, db, User
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Test users to create
TEST_USERS = [
    {
        'username': 'testuser1',
        'email': 'testuser1@example.com',
        'password': 'password123',
        'full_name': 'Test User One',
        'phone': '1234567890'
    },
    {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
        'password': 'password123',
        'full_name': 'Test User Two',
        'phone': '9876543210'
    },
    {
        'username': 'demouser',
        'email': 'demo@aushadham.com',
        'password': 'demo123',
        'full_name': 'Demo User',
        'phone': '5555555555'
    }
]

def seed_users():
    """Create test users in the database"""
    with app.app_context():
        logger.info("Starting user seeding...")
        
        created_count = 0
        skipped_count = 0
        
        for user_data in TEST_USERS:
            # Check if user already exists
            existing_user = User.query.filter(
                (User.username == user_data['username']) | 
                (User.email == user_data['email'])
            ).first()
            
            if existing_user:
                logger.info(f"User '{user_data['username']}' already exists, skipping...")
                skipped_count += 1
                continue
            
            # Create new user
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                full_name=user_data['full_name'],
                phone=user_data['phone']
            )
            user.set_password(user_data['password'])
            
            db.session.add(user)
            logger.info(f"Created user: {user_data['username']} ({user_data['email']})")
            created_count += 1
        
        db.session.commit()
        logger.info(f"\nSeeding complete! Created {created_count} users, skipped {skipped_count} existing users.")
        
        # Display all users
        logger.info("\nAll users in database:")
        all_users = User.query.all()
        for user in all_users:
            logger.info(f"  - {user.username} ({user.email})")

if __name__ == '__main__':
    seed_users()

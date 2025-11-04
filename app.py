from flask import Flask, request, jsonify, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import secrets
import uuid
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv
import logging
from supabase_service import get_supabase_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    logger.warning(f"Could not load .env file: {e}. Using default configuration.")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(16))
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', secrets.token_hex(16))
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///aushadham.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app, supports_credentials=True)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Initialize Supabase service if configured
USE_SUPABASE = os.getenv('USE_SUPABASE', 'false').lower() == 'true'
supabase_service = None

if USE_SUPABASE:
    try:
        supabase_service = get_supabase_service()
        if supabase_service:
            logger.info("Using Supabase for database operations")
        else:
            logger.warning("Supabase configuration found but initialization failed. Falling back to SQLAlchemy.")
            USE_SUPABASE = False
    except Exception as e:
        logger.error(f"Failed to initialize Supabase: {e}. Falling back to SQLAlchemy.")
        USE_SUPABASE = False
else:
    logger.info("Using SQLAlchemy for database operations")

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    saved_questionnaires = db.relationship('SavedQuestionnaire', backref='user', lazy=True, cascade='all, delete-orphan')
    feedback = db.relationship('UserFeedback', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set the password"""
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        """Check if the provided password matches the hash"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SavedQuestionnaire(db.Model):
    __tablename__ = 'saved_questionnaires'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    session_id = db.Column(db.String(100), unique=True, nullable=False)
    symptom = db.Column(db.String(200), nullable=False)
    initial_description = db.Column(db.Text)
    answers = db.Column(db.JSON, nullable=False)
    report = db.Column(db.JSON)
    severity = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert saved questionnaire to dictionary"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'symptom': self.symptom,
            'initial_description': self.initial_description,
            'answers': self.answers,
            'report': self.report,
            'severity': self.severity,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class UserFeedback(db.Model):
    __tablename__ = 'user_feedback'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    questionnaire_id = db.Column(db.Integer, db.ForeignKey('saved_questionnaires.id'), nullable=True)
    rating = db.Column(db.Integer)  # 1-5 star rating
    comment = db.Column(db.Text)
    feedback_type = db.Column(db.String(50))  # 'general', 'questionnaire', 'recommendation'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Convert feedback to dictionary"""
        return {
            'id': self.id,
            'questionnaire_id': self.questionnaire_id,
            'rating': self.rating,
            'comment': self.comment,
            'feedback_type': self.feedback_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# Comprehensive medical questionnaire knowledge base
questionnaire_templates = {
    'stomach': {
        'initial_questions': [
            {
                'id': 'hydration',
                'question': 'Did you drink enough water today (at least 6-8 glasses)?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'recent_meal',
                'question': 'Did you eat anything unusual or outside food in the last 24 hours?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'pain_location',
                'question': 'Is the pain in your upper abdomen or lower abdomen?',
                'type': 'choice',
                'options': ['Upper abdomen', 'Lower abdomen', 'All over', 'Around belly button'],
                'weight': 'high'
            },
            {
                'id': 'pain_type',
                'question': 'How would you describe the pain?',
                'type': 'choice',
                'options': ['Sharp/Stabbing', 'Dull/Aching', 'Cramping', 'Burning'],
                'weight': 'medium'
            },
            {
                'id': 'nausea',
                'question': 'Are you experiencing nausea or have you vomited?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'bowel_movement',
                'question': 'Have you had normal bowel movements today?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'fever',
                'question': 'Do you have a fever or feel feverish?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'exercise',
                'question': 'Were you involved in any strenuous exercise in the last couple of days?',
                'type': 'yes_no',
                'weight': 'low'
            },
            {
                'id': 'stress',
                'question': 'Have you been under unusual stress lately?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'medication',
                'question': 'Have you taken any medication for this pain?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'duration',
                'question': 'How long have you been experiencing this pain?',
                'type': 'choice',
                'options': ['Less than 1 hour', '1-3 hours', '3-6 hours', 'More than 6 hours'],
                'weight': 'high'
            },
            {
                'id': 'severity',
                'question': 'On a scale of 1-10, how severe is your pain?',
                'type': 'scale',
                'options': ['1-3 (Mild)', '4-6 (Moderate)', '7-9 (Severe)', '10 (Unbearable)'],
                'weight': 'high'
            }
        ],
        'conditional_questions': {
            'nausea': {
                'yes': [
                    {
                        'id': 'vomit_frequency',
                        'question': 'How many times have you vomited?',
                        'type': 'choice',
                        'options': ['Once', '2-3 times', 'More than 3 times', 'Just nauseous, no vomiting'],
                        'weight': 'high'
                    }
                ]
            },
            'recent_meal': {
                'yes': [
                    {
                        'id': 'food_type',
                        'question': 'What type of food did you eat?',
                        'type': 'choice',
                        'options': ['Street food', 'Restaurant food', 'Home-cooked but unusual', 'Dairy products'],
                        'weight': 'medium'
                    }
                ]
            }
        }
    },
    'headache': {
        'initial_questions': [
            {
                'id': 'location',
                'question': 'Where exactly is your headache located?',
                'type': 'choice',
                'options': ['Forehead', 'Temples', 'Back of head', 'One side only', 'Entire head'],
                'weight': 'high'
            },
            {
                'id': 'pain_type',
                'question': 'How would you describe the pain?',
                'type': 'choice',
                'options': ['Throbbing/Pulsating', 'Constant pressure', 'Sharp/Stabbing', 'Dull ache'],
                'weight': 'high'
            },
            {
                'id': 'triggers',
                'question': 'Did anything specific trigger this headache?',
                'type': 'choice',
                'options': ['Stress', 'Lack of sleep', 'Bright lights', 'Loud noise', 'Not sure'],
                'weight': 'medium'
            },
            {
                'id': 'light_sensitivity',
                'question': 'Are you sensitive to light right now?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'sound_sensitivity',
                'question': 'Are you sensitive to sound right now?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'nausea',
                'question': 'Do you feel nauseous?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'vision',
                'question': 'Are you experiencing any vision changes (blurriness, spots, auras)?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'frequency',
                'question': 'How often do you get headaches?',
                'type': 'choice',
                'options': ['Rarely', 'Once a month', 'Weekly', 'Daily'],
                'weight': 'medium'
            },
            {
                'id': 'hydration',
                'question': 'Have you been drinking enough water today?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'sleep',
                'question': 'How many hours did you sleep last night?',
                'type': 'choice',
                'options': ['Less than 4', '4-6 hours', '6-8 hours', 'More than 8'],
                'weight': 'medium'
            },
            {
                'id': 'screen_time',
                'question': 'Have you been looking at screens for extended periods today?',
                'type': 'yes_no',
                'weight': 'low'
            },
            {
                'id': 'medication',
                'question': 'Have you taken any pain medication?',
                'type': 'yes_no',
                'weight': 'medium'
            }
        ],
        'conditional_questions': {
            'medication': {
                'yes': [
                    {
                        'id': 'med_effect',
                        'question': 'Did the medication help?',
                        'type': 'choice',
                        'options': ['Yes, completely', 'Partially', 'Not at all', 'Made it worse'],
                        'weight': 'high'
                    }
                ]
            }
        }
    },
    'fever': {
        'initial_questions': [
            {
                'id': 'temperature',
                'question': 'What is your current temperature?',
                'type': 'choice',
                'options': ['98-99°F', '100-101°F', '102-103°F', 'Above 103°F', "Don't know"],
                'weight': 'high'
            },
            {
                'id': 'duration',
                'question': 'How long have you had this fever?',
                'type': 'choice',
                'options': ['Just started', 'Few hours', '1 day', '2-3 days', 'More than 3 days'],
                'weight': 'high'
            },
            {
                'id': 'chills',
                'question': 'Are you experiencing chills or shivering?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'sweating',
                'question': 'Are you sweating excessively?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'body_ache',
                'question': 'Do you have body aches or muscle pain?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'throat',
                'question': 'Do you have a sore throat?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'cough',
                'question': 'Do you have a cough?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'appetite',
                'question': 'Have you lost your appetite?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'fatigue',
                'question': 'Are you feeling unusually tired or weak?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'exposure',
                'question': 'Have you been exposed to anyone who was sick recently?',
                'type': 'yes_no',
                'weight': 'medium'
            }
        ],
        'conditional_questions': {
            'cough': {
                'yes': [
                    {
                        'id': 'cough_type',
                        'question': 'Is your cough dry or producing phlegm?',
                        'type': 'choice',
                        'options': ['Dry cough', 'With phlegm', 'Both'],
                        'weight': 'high'
                    }
                ]
            }
        }
    },
    'cough': {
        'initial_questions': [
            {
                'id': 'cough_type',
                'question': 'Is your cough dry or producing phlegm/mucus?',
                'type': 'choice',
                'options': ['Dry cough', 'With clear phlegm', 'With colored phlegm', 'With blood'],
                'weight': 'high'
            },
            {
                'id': 'duration',
                'question': 'How long have you been coughing?',
                'type': 'choice',
                'options': ['Just started', '2-3 days', '1 week', '2 weeks', 'More than 2 weeks'],
                'weight': 'high'
            },
            {
                'id': 'frequency',
                'question': 'How often are you coughing?',
                'type': 'choice',
                'options': ['Occasionally', 'Frequently', 'Constant', 'Only at night', 'Only in morning'],
                'weight': 'medium'
            },
            {
                'id': 'chest_pain',
                'question': 'Do you have chest pain when coughing?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'breathing',
                'question': 'Are you experiencing shortness of breath?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'wheezing',
                'question': 'Do you hear wheezing when breathing?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'fever',
                'question': 'Do you have a fever?',
                'type': 'yes_no',
                'weight': 'high'
            },
            {
                'id': 'smoking',
                'question': 'Do you smoke or have you been exposed to smoke?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'allergies',
                'question': 'Do you have known allergies?',
                'type': 'yes_no',
                'weight': 'medium'
            },
            {
                'id': 'environment',
                'question': 'Have you been exposed to dust, chemicals, or irritants?',
                'type': 'yes_no',
                'weight': 'medium'
            }
        ],
        'conditional_questions': {}
    }
}

class QuestionnaireSession:
    def __init__(self, session_id: str, symptom: str, initial_description: str):
        self.session_id = session_id
        self.symptom = symptom
        self.initial_description = initial_description
        self.questions = []
        self.current_index = 0
        self.answers = {}
        self.completed = False
        self.start_time = datetime.now()
        self._build_questions()
    
    def _build_questions(self):
        """Build the complete question list based on symptom"""
        template = self._get_template()
        if template:
            self.questions = template.get('initial_questions', [])
    
    def _get_template(self):
        """Get the appropriate questionnaire template"""
        symptom_keywords = {
            'stomach': ['stomach', 'belly', 'abdomen', 'tummy', 'digestive', 'gastric'],
            'headache': ['head', 'headache', 'migraine', 'temple'],
            'fever': ['fever', 'temperature', 'hot', 'feverish'],
            'cough': ['cough', 'coughing', 'throat', 'respiratory']
        }
        
        for key, keywords in symptom_keywords.items():
            if any(word in self.symptom.lower() for word in keywords):
                return questionnaire_templates.get(key)
        
        # Default to stomach if no match
        return questionnaire_templates.get('stomach')
    
    def get_current_question(self):
        """Get the current question"""
        if self.current_index < len(self.questions):
            question = self.questions[self.current_index]
            return {
                'question': question['question'],
                'type': question['type'],
                'options': question.get('options', ['Yes', 'No']),
                'current': self.current_index + 1,
                'total': len(self.questions),
                'progress': ((self.current_index + 1) / len(self.questions)) * 100
            }
        return None
    
    def submit_answer(self, answer: str):
        """Submit answer for current question"""
        if self.current_index < len(self.questions):
            question_id = self.questions[self.current_index]['id']
            self.answers[question_id] = answer
            
            # Check for conditional questions
            self._add_conditional_questions(question_id, answer)
            
            return True
        return False
    
    def _add_conditional_questions(self, question_id: str, answer: str):
        """Add conditional questions based on answer"""
        template = self._get_template()
        if template and 'conditional_questions' in template:
            conditionals = template['conditional_questions'].get(question_id, {})
            if answer.lower() in conditionals:
                new_questions = conditionals[answer.lower()]
                # Insert new questions after current one
                for i, q in enumerate(new_questions):
                    self.questions.insert(self.current_index + 1 + i, q)
    
    def next_question(self):
        """Move to next question"""
        if self.current_index < len(self.questions) - 1:
            self.current_index += 1
            return True
        else:
            self.completed = True
            return False
    
    def previous_question(self):
        """Move to previous question"""
        if self.current_index > 0:
            self.current_index -= 1
            return True
        return False
    
    def skip_question(self):
        """Skip current question"""
        if self.current_index < len(self.questions):
            question_id = self.questions[self.current_index]['id']
            self.answers[question_id] = 'Skipped'
            return self.next_question()
        return False
    
    def generate_report(self):
        """Generate comprehensive report"""
        template = self._get_template()
        
        # Analyze answers for risk assessment
        risk_score = 0
        recommendations = []
        medications = []
        
        for question in self.questions:
            answer = self.answers.get(question['id'], 'Not answered')
            weight = question.get('weight', 'low')
            
            # Calculate risk based on certain answers
            if answer.lower() in ['yes', 'severe', 'more than 3 days', 'above 103°f', '7-9 (severe)', '10 (unbearable)']:
                if weight == 'high':
                    risk_score += 3
                elif weight == 'medium':
                    risk_score += 2
                else:
                    risk_score += 1
        
        # Determine severity
        if risk_score >= 15:
            severity = 'High'
            urgency = 'Seek immediate medical attention'
        elif risk_score >= 8:
            severity = 'Moderate'
            urgency = 'Consult a doctor within 24 hours'
        else:
            severity = 'Low'
            urgency = 'Monitor symptoms, see doctor if worsens'
        
        # Generate recommendations based on symptom type
        if 'stomach' in self.symptom.lower():
            recommendations = [
                'Stay hydrated with small sips of water',
                'Eat bland foods (BRAT diet: Bananas, Rice, Applesauce, Toast)',
                'Avoid dairy, caffeine, and fatty foods',
                'Rest and avoid strenuous activities'
            ]
            medications = [
                {'name': 'Antacids (Tums, Mylanta)', 'purpose': 'For acid reflux or indigestion'},
                {'name': 'Bismuth subsalicylate (Pepto-Bismol)', 'purpose': 'For general stomach upset'},
                {'name': 'Simethicone (Gas-X)', 'purpose': 'For gas and bloating'}
            ]
        elif 'head' in self.symptom.lower():
            recommendations = [
                'Rest in a quiet, dark room',
                'Apply cold compress to forehead',
                'Stay hydrated',
                'Practice relaxation techniques',
                'Maintain regular sleep schedule'
            ]
            medications = [
                {'name': 'Acetaminophen (Tylenol)', 'purpose': 'For mild to moderate pain'},
                {'name': 'Ibuprofen (Advil, Motrin)', 'purpose': 'For inflammation and pain'},
                {'name': 'Aspirin', 'purpose': 'For tension headaches'}
            ]
        elif 'fever' in self.symptom.lower():
            recommendations = [
                'Rest and get plenty of sleep',
                'Stay hydrated with water and electrolyte drinks',
                'Use cool compresses',
                'Wear light clothing',
                'Monitor temperature regularly'
            ]
            medications = [
                {'name': 'Acetaminophen (Tylenol)', 'purpose': 'To reduce fever'},
                {'name': 'Ibuprofen (Advil, Motrin)', 'purpose': 'To reduce fever and body aches'}
            ]
        elif 'cough' in self.symptom.lower():
            recommendations = [
                'Stay hydrated to thin mucus',
                'Use a humidifier',
                'Gargle with warm salt water',
                'Avoid irritants like smoke',
                'Elevate head while sleeping'
            ]
            medications = [
                {'name': 'Dextromethorphan (Robitussin)', 'purpose': 'For dry cough'},
                {'name': 'Guaifenesin (Mucinex)', 'purpose': 'For productive cough'},
                {'name': 'Throat lozenges', 'purpose': 'For throat irritation'}
            ]
        
        return {
            'session_id': self.session_id,
            'symptom': self.symptom,
            'initial_description': self.initial_description,
            'assessment_date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'questions_answered': len([a for a in self.answers.values() if a != 'Skipped']),
            'total_questions': len(self.questions),
            'severity': severity,
            'urgency': urgency,
            'risk_score': risk_score,
            'recommendations': recommendations,
            'suggested_medications': medications,
            'answers': self.answers,
            'detailed_answers': [
                {
                    'question': q['question'],
                    'answer': self.answers.get(q['id'], 'Not answered'),
                    'importance': q.get('weight', 'low')
                } for q in self.questions
            ],
            'disclaimer': 'This assessment is for informational purposes only and does not replace professional medical advice. Please consult a healthcare provider for proper diagnosis and treatment.'
        }

# Session storage
sessions: Dict[str, QuestionnaireSession] = {}

# Authentication Routes
@app.route("/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.json
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('full_name', '')
        phone = data.get('phone', '')
        
        # Validate required fields
        if not username or not email or not password:
            return jsonify({'success': False, 'error': 'Username, email, and password are required'}), 400
        
        if USE_SUPABASE:
            # Using Supabase
            # Check if user already exists
            if supabase_service.get_user_by_username(username):
                return jsonify({'success': False, 'error': 'Username already exists'}), 409
            
            if supabase_service.get_user_by_email(email):
                return jsonify({'success': False, 'error': 'Email already exists'}), 409
            
            # Create new user
            user = supabase_service.create_user(username, email, password, full_name, phone)
            if not user:
                return jsonify({'success': False, 'error': 'Registration failed. Please try again.'}), 400
            
            # Create access token
            access_token = create_access_token(identity=user['id'])
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user.get('full_name', ''),
                    'phone': user.get('phone', ''),
                    'created_at': user.get('created_at')
                },
                'access_token': access_token
            }), 201
        else:
            # Using SQLAlchemy
            # Check if user already exists
            if User.query.filter_by(username=username).first():
                return jsonify({'success': False, 'error': 'Username already exists'}), 409
            
            if User.query.filter_by(email=email).first():
                return jsonify({'success': False, 'error': 'Email already exists'}), 409
            
            # Create new user
            user = User(
                username=username,
                email=email,
                full_name=full_name,
                phone=phone
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user': user.to_dict(),
                'access_token': access_token
            }), 201
    except Exception as e:
        if not USE_SUPABASE:
            db.session.rollback()
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'success': False, 'error': 'Registration failed. Please try again.'}), 400

@app.route("/login", methods=["POST"])
def login():
    """Login a user"""
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'success': False, 'error': 'Username and password are required'}), 400
        
        if USE_SUPABASE:
            # Using Supabase
            # Find user by username or email
            user = supabase_service.get_user_by_username(username)
            if not user:
                user = supabase_service.get_user_by_email(username)
            
            if not user or not supabase_service.verify_password(password, user['password_hash']):
                return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
            
            # Create access token
            access_token = create_access_token(identity=user['id'])
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user.get('full_name', ''),
                    'phone': user.get('phone', ''),
                    'created_at': user.get('created_at')
                },
                'access_token': access_token
            })
        else:
            # Using SQLAlchemy
            # Find user by username or email
            user = User.query.filter(
                (User.username == username) | (User.email == username)
            ).first()
            
            if not user or not user.check_password(password):
                return jsonify({'success': False, 'error': 'Invalid username or password'}), 401
            
            # Create access token
            access_token = create_access_token(identity=user.id)
            
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'user': user.to_dict(),
                'access_token': access_token
            })
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'success': False, 'error': 'Login failed. Please try again.'}), 400

@app.route("/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        user_id = get_jwt_identity()
        
        if USE_SUPABASE:
            user = supabase_service.get_user_by_id(user_id)
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            return jsonify({
                'success': True,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'full_name': user.get('full_name', ''),
                    'phone': user.get('phone', ''),
                    'created_at': user.get('created_at')
                }
            })
        else:
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            return jsonify({
                'success': True,
                'user': user.to_dict()
            })
    except Exception as e:
        logger.error(f"Get profile error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to retrieve profile.'}), 400

@app.route("/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update user profile"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        if USE_SUPABASE:
            user = supabase_service.get_user_by_id(user_id)
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            updates = {}
            if 'full_name' in data:
                updates['full_name'] = data['full_name']
            if 'phone' in data:
                updates['phone'] = data['phone']
            if 'email' in data:
                # Check if email is already taken by another user
                existing = supabase_service.get_user_by_email(data['email'])
                if existing and existing['id'] != user_id:
                    return jsonify({'success': False, 'error': 'Email already in use'}), 409
                updates['email'] = data['email']
            
            updated_user = supabase_service.update_user(user_id, updates)
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'user': {
                    'id': updated_user['id'],
                    'username': updated_user['username'],
                    'email': updated_user['email'],
                    'full_name': updated_user.get('full_name', ''),
                    'phone': updated_user.get('phone', ''),
                    'created_at': updated_user.get('created_at')
                }
            })
        else:
            user = User.query.get(user_id)
            
            if not user:
                return jsonify({'success': False, 'error': 'User not found'}), 404
            
            # Update allowed fields
            if 'full_name' in data:
                user.full_name = data['full_name']
            if 'phone' in data:
                user.phone = data['phone']
            if 'email' in data:
                # Check if email is already taken by another user
                existing = User.query.filter(User.email == data['email'], User.id != user_id).first()
                if existing:
                    return jsonify({'success': False, 'error': 'Email already in use'}), 409
                user.email = data['email']
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Profile updated successfully',
                'user': user.to_dict()
            })
    except Exception as e:
        if not USE_SUPABASE:
            db.session.rollback()
        logger.error(f"Profile update error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to update profile.'}), 400

# Questionnaire Management Routes
@app.route("/save_questionnaire", methods=["POST"])
@jwt_required()
def save_questionnaire():
    """Save a completed questionnaire for the user"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        session_id = data.get('session_id')
        
        if not session_id or session_id not in sessions:
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        session_obj = sessions[session_id]
        
        # Generate report if not already done
        report = session_obj.generate_report()
        
        if USE_SUPABASE:
            # Check if already saved
            existing = supabase_service.get_questionnaire_by_session_id(session_id)
            if existing:
                return jsonify({'success': False, 'error': 'Questionnaire already saved'}), 409
            
            # Save to Supabase
            saved = supabase_service.save_questionnaire(
                user_id=user_id,
                session_id=session_id,
                symptom=session_obj.symptom,
                initial_description=session_obj.initial_description,
                answers=session_obj.answers,
                report=report,
                severity=report.get('severity', 'Unknown')
            )
            
            return jsonify({
                'success': True,
                'message': 'Questionnaire saved successfully',
                'questionnaire': {
                    'id': saved['id'],
                    'session_id': saved['session_id'],
                    'symptom': saved['symptom'],
                    'initial_description': saved.get('initial_description'),
                    'answers': saved['answers'],
                    'report': saved.get('report'),
                    'severity': saved.get('severity'),
                    'created_at': saved.get('created_at')
                }
            }), 201
        else:
            # Check if already saved
            existing = SavedQuestionnaire.query.filter_by(session_id=session_id).first()
            if existing:
                return jsonify({'success': False, 'error': 'Questionnaire already saved'}), 409
            
            # Save to database
            saved = SavedQuestionnaire(
                user_id=user_id,
                session_id=session_id,
                symptom=session_obj.symptom,
                initial_description=session_obj.initial_description,
                answers=session_obj.answers,
                report=report,
                severity=report.get('severity', 'Unknown')
            )
            
            db.session.add(saved)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Questionnaire saved successfully',
                'questionnaire': saved.to_dict()
            }), 201
    except Exception as e:
        if not USE_SUPABASE:
            db.session.rollback()
        logger.error(f"Save questionnaire error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to save questionnaire.'}), 400

@app.route("/my_questionnaires", methods=["GET"])
@jwt_required()
def get_my_questionnaires():
    """Get all questionnaires for the current user"""
    try:
        user_id = get_jwt_identity()
        
        if USE_SUPABASE:
            questionnaires = supabase_service.get_user_questionnaires(user_id)
            formatted_questionnaires = [
                {
                    'id': q['id'],
                    'session_id': q['session_id'],
                    'symptom': q['symptom'],
                    'initial_description': q.get('initial_description'),
                    'answers': q['answers'],
                    'report': q.get('report'),
                    'severity': q.get('severity'),
                    'created_at': q.get('created_at')
                } for q in questionnaires
            ]
            
            return jsonify({
                'success': True,
                'questionnaires': formatted_questionnaires,
                'count': len(formatted_questionnaires)
            })
        else:
            questionnaires = SavedQuestionnaire.query.filter_by(user_id=user_id).order_by(SavedQuestionnaire.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'questionnaires': [q.to_dict() for q in questionnaires],
                'count': len(questionnaires)
            })
    except Exception as e:
        logger.error(f"Get questionnaires error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to retrieve questionnaires.'}), 400

@app.route("/my_questionnaires/<int:questionnaire_id>", methods=["GET"])
@jwt_required()
def get_questionnaire_detail(questionnaire_id):
    """Get details of a specific questionnaire"""
    try:
        user_id = get_jwt_identity()
        
        if USE_SUPABASE:
            questionnaire = supabase_service.get_questionnaire_by_id(questionnaire_id, user_id)
            
            if not questionnaire:
                return jsonify({'success': False, 'error': 'Questionnaire not found'}), 404
            
            return jsonify({
                'success': True,
                'questionnaire': {
                    'id': questionnaire['id'],
                    'session_id': questionnaire['session_id'],
                    'symptom': questionnaire['symptom'],
                    'initial_description': questionnaire.get('initial_description'),
                    'answers': questionnaire['answers'],
                    'report': questionnaire.get('report'),
                    'severity': questionnaire.get('severity'),
                    'created_at': questionnaire.get('created_at')
                }
            })
        else:
            questionnaire = SavedQuestionnaire.query.filter_by(id=questionnaire_id, user_id=user_id).first()
            
            if not questionnaire:
                return jsonify({'success': False, 'error': 'Questionnaire not found'}), 404
            
            return jsonify({
                'success': True,
                'questionnaire': questionnaire.to_dict()
            })
    except Exception as e:
        logger.error(f"Get questionnaire detail error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to retrieve questionnaire.'}), 400

@app.route("/my_questionnaires/<int:questionnaire_id>", methods=["DELETE"])
@jwt_required()
def delete_questionnaire(questionnaire_id):
    """Delete a specific questionnaire"""
    try:
        user_id = get_jwt_identity()
        
        if USE_SUPABASE:
            questionnaire = supabase_service.get_questionnaire_by_id(questionnaire_id, user_id)
            
            if not questionnaire:
                return jsonify({'success': False, 'error': 'Questionnaire not found'}), 404
            
            supabase_service.delete_questionnaire(questionnaire_id, user_id)
            
            return jsonify({
                'success': True,
                'message': 'Questionnaire deleted successfully'
            })
        else:
            questionnaire = SavedQuestionnaire.query.filter_by(id=questionnaire_id, user_id=user_id).first()
            
            if not questionnaire:
                return jsonify({'success': False, 'error': 'Questionnaire not found'}), 404
            
            db.session.delete(questionnaire)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Questionnaire deleted successfully'
            })
    except Exception as e:
        if not USE_SUPABASE:
            db.session.rollback()
        logger.error(f"Delete questionnaire error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to delete questionnaire.'}), 400

# Feedback Routes
@app.route("/feedback", methods=["POST"])
@jwt_required()
def submit_feedback():
    """Submit feedback"""
    try:
        user_id = get_jwt_identity()
        data = request.json
        
        rating = data.get('rating')
        comment = data.get('comment', '')
        feedback_type = data.get('feedback_type', 'general')
        questionnaire_id = data.get('questionnaire_id')
        
        # Validate rating (must be provided and between 1-5)
        if rating is not None and (rating < 1 or rating > 5):
            return jsonify({'success': False, 'error': 'Rating must be between 1 and 5'}), 400
        
        if USE_SUPABASE:
            # If questionnaire_id is provided, verify it belongs to the user
            if questionnaire_id:
                questionnaire = supabase_service.get_questionnaire_by_id(questionnaire_id, user_id)
                if not questionnaire:
                    return jsonify({'success': False, 'error': 'Questionnaire not found'}), 404
            
            feedback = supabase_service.create_feedback(
                user_id=user_id,
                questionnaire_id=questionnaire_id,
                rating=rating,
                comment=comment,
                feedback_type=feedback_type
            )
            
            return jsonify({
                'success': True,
                'message': 'Feedback submitted successfully',
                'feedback': {
                    'id': feedback['id'],
                    'questionnaire_id': feedback.get('questionnaire_id'),
                    'rating': feedback.get('rating'),
                    'comment': feedback.get('comment'),
                    'feedback_type': feedback.get('feedback_type'),
                    'created_at': feedback.get('created_at')
                }
            }), 201
        else:
            # If questionnaire_id is provided, verify it belongs to the user
            if questionnaire_id:
                questionnaire = SavedQuestionnaire.query.filter_by(id=questionnaire_id, user_id=user_id).first()
                if not questionnaire:
                    return jsonify({'success': False, 'error': 'Questionnaire not found'}), 404
            
            feedback = UserFeedback(
                user_id=user_id,
                questionnaire_id=questionnaire_id,
                rating=rating,
                comment=comment,
                feedback_type=feedback_type
            )
            
            db.session.add(feedback)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Feedback submitted successfully',
                'feedback': feedback.to_dict()
            }), 201
    except Exception as e:
        if not USE_SUPABASE:
            db.session.rollback()
        logger.error(f"Submit feedback error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to submit feedback.'}), 400

@app.route("/my_feedback", methods=["GET"])
@jwt_required()
def get_my_feedback():
    """Get all feedback submitted by the current user"""
    try:
        user_id = get_jwt_identity()
        
        if USE_SUPABASE:
            feedback_list = supabase_service.get_user_feedback(user_id)
            formatted_feedback = [
                {
                    'id': f['id'],
                    'questionnaire_id': f.get('questionnaire_id'),
                    'rating': f.get('rating'),
                    'comment': f.get('comment'),
                    'feedback_type': f.get('feedback_type'),
                    'created_at': f.get('created_at')
                } for f in feedback_list
            ]
            
            return jsonify({
                'success': True,
                'feedback': formatted_feedback,
                'count': len(formatted_feedback)
            })
        else:
            feedback_list = UserFeedback.query.filter_by(user_id=user_id).order_by(UserFeedback.created_at.desc()).all()
            
            return jsonify({
                'success': True,
                'feedback': [f.to_dict() for f in feedback_list],
                'count': len(feedback_list)
            })
    except Exception as e:
        logger.error(f"Get feedback error: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to retrieve feedback.'}), 400

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Medical Questionnaire API is running!",
        "version": "4.0",
        "features": ["User Authentication", "Save Questionnaires", "Feedback System"],
        "endpoints": {
            "authentication": [
                "/register (POST)",
                "/login (POST)",
                "/profile (GET, PUT)"
            ],
            "questionnaire": [
                "/start_questionnaire (POST)",
                "/submit_answer (POST)", 
                "/get_current_question (POST)",
                "/get_report (POST)",
                "/save_questionnaire (POST) [Auth Required]",
                "/my_questionnaires (GET) [Auth Required]",
                "/my_questionnaires/<id> (GET, DELETE) [Auth Required]"
            ],
            "feedback": [
                "/feedback (POST) [Auth Required]",
                "/my_feedback (GET) [Auth Required]"
            ],
            "health": [
                "/health_check (GET)"
            ]
        }
    })

@app.route("/start_questionnaire", methods=["POST"])
def start_questionnaire():
    try:
        data = request.json
        symptom = data.get('symptom', '')
        initial_description = data.get('description', symptom)
        
        # Generate unique session ID
        session_id = str(uuid.uuid4())
        
        # Create new questionnaire session
        session = QuestionnaireSession(session_id, symptom, initial_description)
        sessions[session_id] = session
        
        # Get first question
        first_question = session.get_current_question()
        
        return jsonify({
            'success': True,
            'session_id': session_id,
            'message': f'Starting questionnaire for: {symptom}',
            'question': first_question
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route("/submit_answer", methods=["POST"])
def submit_answer():
    try:
        data = request.json
        session_id = data.get('session_id')
        answer = data.get('answer')
        action = data.get('action', 'next')  # next, previous, or skip
        
        if session_id not in sessions:
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        session = sessions[session_id]
        
        # Submit answer if not navigating back
        if action != 'previous':
            session.submit_answer(answer)
        
        # Handle navigation
        if action == 'next':
            has_next = session.next_question()
        elif action == 'previous':
            has_next = session.previous_question()
        elif action == 'skip':
            has_next = session.skip_question()
        else:
            has_next = True
        
        # Check if questionnaire is completed
        if session.completed:
            return jsonify({
                'success': True,
                'completed': True,
                'message': 'Questionnaire completed!',
                'session_id': session_id
            })
        
        # Get current question
        current_question = session.get_current_question()
        
        return jsonify({
            'success': True,
            'completed': False,
            'question': current_question
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route("/get_current_question", methods=["POST"])
def get_current_question():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        session = sessions[session_id]
        current_question = session.get_current_question()
        
        return jsonify({
            'success': True,
            'question': current_question,
            'completed': session.completed
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route("/get_report", methods=["POST"])
def get_report():
    try:
        data = request.json
        session_id = data.get('session_id')
        
        if session_id not in sessions:
            return jsonify({'success': False, 'error': 'Invalid session'}), 404
        
        session = sessions[session_id]
        report = session.generate_report()
        
        # Clean up session after generating report
        # del sessions[session_id]
        
        return jsonify({
            'success': True,
            'report': report
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route("/health_check", methods=["GET"])
def health_check():
    return jsonify({
        'status': 'healthy',
        'active_sessions': len(sessions),
        'timestamp': datetime.now().isoformat()
    })

if __name__ == "__main__":
    # Create database tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
    
    app.run(debug=True)
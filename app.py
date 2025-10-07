from flask import Flask, request, jsonify, session
from flask_cors import CORS
import secrets
import uuid
from datetime import datetime
from typing import Dict, List, Optional

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app, supports_credentials=True)

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

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Medical Questionnaire API is running!",
        "version": "3.0",
        "endpoints": [
            "/start_questionnaire",
            "/submit_answer", 
            "/next_question",
            "/previous_question",
            "/skip_question",
            "/get_current_question",
            "/get_report"
        ]
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
    app.run(debug=True)
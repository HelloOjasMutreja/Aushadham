from flask import Flask, request, jsonify, session
from flask_cors import CORS
import secrets
import re
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app, supports_credentials=True)

# Enhanced medical knowledge base
medical_knowledge = {
    'headache': {
        'follow_up_questions': [
            "How severe is your headache on a scale of 1-10?",
            "Where exactly is the pain located? (forehead, temples, back of head, entire head)",
            "How long have you been experiencing this headache?",
            "Is it throbbing, constant, or sharp pain?",
            "Do you have any sensitivity to light or sound?"
        ],
        'conditions': {
            'migraine': {
                'indicators': ['severe', 'throbbing', 'one side', 'light sensitivity', 'nausea'],
                'medicine': 'Sumatriptan (Imitrex) or Ibuprofen',
                'dosage': {
                    'adults': 'Sumatriptan: 50-100mg at onset; Ibuprofen: 400-600mg',
                    'children': 'Consult pediatrician for migraine medication'
                },
                'advice': 'Rest in a dark, quiet room. Apply cold compress. Stay hydrated.'
            },
            'tension': {
                'indicators': ['mild', 'moderate', 'both sides', 'constant', 'stress'],
                'medicine': 'Acetaminophen (Tylenol) or Aspirin',
                'dosage': {
                    'adults': 'Acetaminophen: 500-1000mg every 4-6 hours; Aspirin: 325-650mg every 4 hours',
                    'children': 'Acetaminophen: 10-15mg/kg every 4-6 hours'
                },
                'advice': 'Practice relaxation techniques. Maintain good posture. Get adequate sleep.'
            }
        }
    },
    'fever': {
        'follow_up_questions': [
            "What is your current temperature?",
            "How long have you had this fever?",
            "Do you have any other symptoms like cough, body aches, or sore throat?",
            "Have you taken any medication already?",
            "Do you have any chronic health conditions?"
        ],
        'conditions': {
            'viral_fever': {
                'indicators': ['mild', '100-102F', 'body aches', 'fatigue'],
                'medicine': 'Acetaminophen (Tylenol) or Ibuprofen (Advil)',
                'dosage': {
                    'adults': 'Acetaminophen: 650-1000mg every 4-6 hours; Ibuprofen: 400-600mg every 6 hours',
                    'children': 'Weight-based dosing - consult package or pediatrician'
                },
                'advice': 'Rest, stay hydrated, use cool compresses. See doctor if fever exceeds 103°F or lasts >3 days.'
            }
        }
    },
    'cough': {
        'follow_up_questions': [
            "Is your cough dry or producing phlegm?",
            "How long have you been coughing?",
            "Is it worse at night or during the day?",
            "Do you have any chest pain or shortness of breath?",
            "Are you a smoker or have allergies?"
        ],
        'conditions': {
            'dry_cough': {
                'indicators': ['dry', 'no phlegm', 'tickling', 'night'],
                'medicine': 'Dextromethorphan (Robitussin DM) or Honey',
                'dosage': {
                    'adults': 'Dextromethorphan: 10-20mg every 4 hours; Honey: 1-2 tablespoons',
                    'children': 'Age 4+: 5-10mg every 4 hours; Honey for age 1+'
                },
                'advice': 'Use humidifier, avoid irritants, stay hydrated, elevate head while sleeping.'
            },
            'productive_cough': {
                'indicators': ['phlegm', 'mucus', 'chest congestion'],
                'medicine': 'Guaifenesin (Mucinex)',
                'dosage': {
                    'adults': '200-400mg every 4 hours',
                    'children': 'Age 4+: 50-100mg every 4 hours'
                },
                'advice': 'Drink plenty of fluids, use steam inhalation, avoid suppressing productive coughs.'
            }
        }
    },
    'stomach': {
        'follow_up_questions': [
            "What kind of stomach issue are you experiencing? (pain, nausea, diarrhea, constipation)",
            "Where exactly is the discomfort?",
            "When did this start?",
            "Have you eaten anything unusual recently?",
            "On a scale of 1-10, how severe is the discomfort?"
        ],
        'conditions': {
            'indigestion': {
                'indicators': ['bloating', 'fullness', 'upper abdomen', 'after eating'],
                'medicine': 'Tums or Pepto-Bismol',
                'dosage': {
                    'adults': 'Tums: 2-4 tablets as needed; Pepto: 30ml every 30 min as needed',
                    'children': 'Consult pediatrician for appropriate antacid'
                },
                'advice': 'Eat smaller meals, avoid spicy/fatty foods, dont lie down after eating.'
            }
        }
    }
}

# Conversation state management
conversations = {}

class HealthChatbot:
    def __init__(self, session_id):
        self.session_id = session_id
        self.state = 'greeting'
        self.current_symptom = None
        self.question_index = 0
        self.collected_info = {}
        self.identified_condition = None
        
    def process_message(self, user_input):
        user_input = user_input.lower().strip()
        
        if self.state == 'greeting':
            return self.handle_greeting(user_input)
        elif self.state == 'symptom_collection':
            return self.handle_symptom_collection(user_input)
        elif self.state == 'asking_questions':
            return self.handle_question_response(user_input)
        elif self.state == 'diagnosis':
            return self.handle_diagnosis_feedback(user_input)
        else:
            return self.handle_greeting(user_input)
    
    def handle_greeting(self, user_input):
        greetings = ['hi', 'hello', 'hey', 'help', 'start']
        if any(greet in user_input for greet in greetings):
            self.state = 'symptom_collection'
            return {
                'response': (
                    "Hello! I'm your AI health assistant. 🏥\n\n"
                    "I can help you with common symptoms like:\n"
                    "• Headache\n"
                    "• Fever\n"
                    "• Cough\n"
                    "• Stomach issues\n\n"
                    "Please describe your main symptom, and I'll ask you some questions to better understand your condition."
                ),
                'quick_replies': ['Headache', 'Fever', 'Cough', 'Stomach pain']
            }
        else:
            # Try to identify symptom directly
            return self.handle_symptom_collection(user_input)
    
    def handle_symptom_collection(self, user_input):
        # Check for main symptoms
        for symptom, data in medical_knowledge.items():
            if symptom in user_input or (symptom == 'stomach' and any(s in user_input for s in ['stomach', 'belly', 'abdomen', 'digestive'])):
                self.current_symptom = symptom
                self.state = 'asking_questions'
                self.question_index = 0
                self.collected_info = {'main_symptom': symptom, 'initial_description': user_input}
                
                return {
                    'response': f"I understand you're experiencing {symptom} issues. Let me ask you a few questions to better help you.\n\n{data['follow_up_questions'][0]}",
                    'quick_replies': self.get_quick_replies_for_question(symptom, 0)
                }
        
        # Symptom not recognized
        self.state = 'symptom_collection'
        return {
            'response': (
                "I can help you with the following symptoms:\n"
                "• Headache\n"
                "• Fever\n"
                "• Cough\n"
                "• Stomach issues\n\n"
                "Please select or describe one of these symptoms."
            ),
            'quick_replies': ['Headache', 'Fever', 'Cough', 'Stomach issues']
        }
    
    def handle_question_response(self, user_input):
        # Store the response
        question_key = f"question_{self.question_index}"
        self.collected_info[question_key] = user_input
        
        # Move to next question
        self.question_index += 1
        questions = medical_knowledge[self.current_symptom]['follow_up_questions']
        
        if self.question_index < len(questions):
            # Ask next question
            return {
                'response': questions[self.question_index],
                'quick_replies': self.get_quick_replies_for_question(self.current_symptom, self.question_index)
            }
        else:
            # All questions asked, provide diagnosis
            return self.provide_diagnosis()
    
    def get_quick_replies_for_question(self, symptom, question_index):
        # Provide context-appropriate quick replies
        quick_reply_options = {
            'headache': {
                0: ['Mild (1-3)', 'Moderate (4-6)', 'Severe (7-10)'],
                1: ['Forehead', 'Temples', 'Back of head', 'Entire head'],
                2: ['Just started', 'Few hours', '1-2 days', 'More than 3 days'],
                3: ['Throbbing', 'Constant', 'Sharp', 'Dull'],
                4: ['Yes, very sensitive', 'Somewhat sensitive', 'No sensitivity']
            },
            'fever': {
                0: ['98-99°F', '100-101°F', '102-103°F', 'Above 103°F'],
                1: ['Just today', '1-2 days', '3-4 days', 'More than 5 days'],
                2: ['Yes, cough', 'Body aches', 'Sore throat', 'No other symptoms'],
                3: ['Yes', 'No'],
                4: ['Yes', 'No']
            },
            'cough': {
                0: ['Dry cough', 'With phlegm', 'Both'],
                1: ['Just started', '2-3 days', 'A week', 'More than a week'],
                2: ['Worse at night', 'Worse during day', 'Same throughout'],
                3: ['Yes, chest pain', 'Shortness of breath', 'Both', 'Neither'],
                4: ['Smoker', 'Have allergies', 'Both', 'Neither']
            },
            'stomach': {
                0: ['Pain', 'Nausea', 'Diarrhea', 'Constipation', 'Bloating'],
                1: ['Upper abdomen', 'Lower abdomen', 'All over', 'Around belly button'],
                2: ['Just now', 'Few hours ago', 'Yesterday', 'Few days ago'],
                3: ['Yes', 'No', 'Not sure'],
                4: ['Mild (1-3)', 'Moderate (4-6)', 'Severe (7-10)']
            }
        }
        
        return quick_reply_options.get(symptom, {}).get(question_index, [])
    
    def provide_diagnosis(self):
        self.state = 'diagnosis'
        
        # Analyze collected information
        symptom_data = medical_knowledge[self.current_symptom]
        
        # Simple diagnosis logic (can be enhanced with more sophisticated analysis)
        # For demo, we'll select the first matching condition
        diagnosis = None
        for condition_name, condition_data in symptom_data['conditions'].items():
            # Check if any indicators match the collected responses
            matches = 0
            for response in self.collected_info.values():
                if isinstance(response, str):
                    for indicator in condition_data['indicators']:
                        if indicator in response.lower():
                            matches += 1
            
            if matches > 0:
                diagnosis = condition_data
                self.identified_condition = condition_name
                break
        
        if not diagnosis:
            # Default to first condition if no specific match
            first_condition = list(symptom_data['conditions'].keys())[0]
            diagnosis = symptom_data['conditions'][first_condition]
            self.identified_condition = first_condition
        
        response_text = (
            "📋 **Based on your responses, here's my assessment:**\n\n"
            f"**Likely Condition:** {self.identified_condition.replace('_', ' ').title()}\n\n"
            f"💊 **Recommended Medication:**\n{diagnosis['medicine']}\n\n"
            f"📊 **Dosage Guidelines:**\n"
            f"• Adults: {diagnosis['dosage']['adults']}\n"
            f"• Children: {diagnosis['dosage']['children']}\n\n"
            f"💡 **Additional Advice:**\n{diagnosis['advice']}\n\n"
            "⚠️ **Important:** This is general guidance only. If symptoms persist or worsen, "
            "please consult a healthcare professional immediately.\n\n"
            "Would you like to check another symptom or need more information?"
        )
        
        return {
            'response': response_text,
            'quick_replies': ['Check another symptom', 'More info', 'Thank you']
        }
    
    def handle_diagnosis_feedback(self, user_input):
        if 'another' in user_input or 'new' in user_input or 'different' in user_input:
            self.state = 'symptom_collection'
            self.current_symptom = None
            self.question_index = 0
            self.collected_info = {}
            return {
                'response': "Sure! Please describe your symptom, and I'll help you with that.",
                'quick_replies': ['Headache', 'Fever', 'Cough', 'Stomach pain']
            }
        elif 'more' in user_input or 'info' in user_input:
            return {
                'response': (
                    "Here's additional information:\n\n"
                    "**When to see a doctor immediately:**\n"
                    "• Severe symptoms that don't improve with medication\n"
                    "• Difficulty breathing or chest pain\n"
                    "• High fever (>103°F) lasting more than 3 days\n"
                    "• Signs of dehydration\n"
                    "• Persistent vomiting or severe abdominal pain\n\n"
                    "**General wellness tips:**\n"
                    "• Stay hydrated (8+ glasses of water daily)\n"
                    "• Get 7-9 hours of sleep\n"
                    "• Maintain a balanced diet\n"
                    "• Exercise regularly\n"
                    "• Manage stress through relaxation techniques\n\n"
                    "Is there anything else I can help you with?"
                ),
                'quick_replies': ['Check another symptom', 'Thank you']
            }
        else:
            self.state = 'greeting'
            return {
                'response': "You're welcome! Take care of yourself, and don't hesitate to seek professional medical help if needed. Feel better soon! 🌟",
                'quick_replies': ['Start over']
            }

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "Advanced Health Chatbot API is running!",
        "version": "2.0",
        "endpoints": ["/get_response", "/reset_session"]
    })

@app.route("/get_response", methods=["POST", "OPTIONS"])
def get_response():
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    user_input = request.json.get('user_input', '')
    session_id = request.json.get('session_id', 'default')
    
    # Get or create chatbot instance for this session
    if session_id not in conversations:
        conversations[session_id] = HealthChatbot(session_id)
    
    chatbot = conversations[session_id]
    response_data = chatbot.process_message(user_input)
    
    return jsonify(response_data)

@app.route("/reset_session", methods=["POST"])
def reset_session():
    session_id = request.json.get('session_id', 'default')
    if session_id in conversations:
        del conversations[session_id]
    return jsonify({"status": "Session reset successfully"})

if __name__ == "__main__":
    app.run(debug=True)
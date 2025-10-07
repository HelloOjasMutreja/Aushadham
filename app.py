from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Enable CORS for all routes
CORS(app)

# --- Medications and chatbot logic (simplified version) ---
medications_data = {
    'common cold': {
        'medicine': 'Acetaminophen (Tylenol)',
        'link': 'https://www.tylenol.com/products/tylenol-extra-strength-caplets',
        'dosage': {
            'adults': '500-1000 mg every 4-6 hours as needed, max 4000 mg/day',
            'children': '10-15 mg/kg every 4-6 hours as needed, max 5 doses/day'
        },
        'when_to_take': 'Take when experiencing symptoms such as headache, fever, or sore throat.'
    },
    'flu': {
        'medicine': 'Oseltamivir (Tamiflu) or Ibuprofen',
        'link': 'https://www.tamiflu.com/',
        'dosage': {
            'adults': 'Tamiflu: 75mg twice daily for 5 days; Ibuprofen: 400-600mg every 6 hours',
            'children': 'Tamiflu: Weight-based dosing; Ibuprofen: 10mg/kg every 6-8 hours'
        },
        'when_to_take': 'Start Tamiflu within 48 hours of symptom onset. Take Ibuprofen for fever and body aches.'
    },
    'allergies': {
        'medicine': 'Cetirizine (Zyrtec) or Loratadine (Claritin)',
        'link': 'https://www.zyrtec.com/',
        'dosage': {
            'adults': '10mg once daily',
            'children': '5mg once daily for ages 2-5, 10mg for ages 6+'
        },
        'when_to_take': 'Take daily during allergy season or when exposed to allergens.'
    }
}

def identify_disease(symptoms):
    symptoms = symptoms.lower()
    
    # Common cold symptoms
    if any(s in symptoms for s in ['cough', 'sore throat', 'runny nose', 'sneezing']):
        if 'fever' not in symptoms or 'mild fever' in symptoms:
            return 'common cold'
    
    # Flu symptoms
    if any(s in symptoms for s in ['high fever', 'body aches', 'fatigue', 'chills']):
        return 'flu'
    
    # Allergy symptoms
    if any(s in symptoms for s in ['itchy eyes', 'sneezing', 'runny nose', 'nasal congestion']):
        if 'fever' not in symptoms:
            return 'allergies'
    
    return None

@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "Health Chatbot API is running!", "endpoints": ["/get_response"]})

@app.route("/get_response", methods=["POST", "OPTIONS"])
def get_response():
    # Handle OPTIONS request for CORS preflight
    if request.method == "OPTIONS":
        return jsonify({}), 200
    
    user_input = request.form.get('user_input', '').lower()
    
    if user_input in ['hi', 'hello', 'hey']:
        return jsonify({"response": "Hello! Please enter your symptoms separated by commas (for example: 'fever, cough, sore throat')."})
    
    if user_input in ['bye', 'goodbye', 'exit']:
        return jsonify({"response": "Goodbye! Take care and consult a healthcare professional if symptoms persist."})
    
    result_disease = identify_disease(user_input)
    
    if result_disease:
        med = medications_data[result_disease]
        response_text = (
            f"Based on your symptoms, it seems you might have {result_disease.title()}.\n\n"
            f"📋 Recommended medicine: {med['medicine']}\n\n"
            f"💊 Dosage for adults: {med['dosage']['adults']}\n"
            f"👶 Dosage for children: {med['dosage']['children']}\n\n"
            f"⏰ When to take: {med['when_to_take']}\n\n"
            f"🔗 More info: {med['link']}\n\n"
            f"⚠️ Note: This is general information only. Please consult a healthcare professional for proper diagnosis and treatment."
        )
    else:
        response_text = (
            "I couldn't identify a specific condition based on your symptoms. "
            "This could mean:\n"
            "• Your symptoms need professional evaluation\n"
            "• You may have a condition not in my database\n"
            "• More specific symptom description might help\n\n"
            "Please consult a healthcare professional for proper diagnosis."
        )

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)
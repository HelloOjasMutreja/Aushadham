from flask import Flask, request, jsonify

app = Flask(__name__)

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
    }
    # You can expand this dictionary with other diseases
}

def identify_disease(symptoms):
    if 'cough' in symptoms or 'fever' in symptoms or 'sore throat' in symptoms:
        return 'common cold'
    return None

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.form.get('user_input', '').lower()
    
    if user_input in ['hello']:
        return jsonify({"response": "Please enter your symptoms separated by commas (for example, 'fever, cough')."})
    if user_input in ['bye']:
        return jsonify({"response": "Goodbye!"})
    
    result_disease = identify_disease(user_input)
    
    if result_disease:
        med = medications_data[result_disease]
        response_text = (
            f"Based on your symptoms, it seems you might have {result_disease.title()}.\n"
            f"Recommended medicine: {med['medicine']}\n"
            f"Dosage for adults: {med['dosage']['adults']}\n"
            f"Dosage for children: {med['dosage']['children']}\n"
            f"When to take: {med['when_to_take']}\n"
            f"More info: {med['link']}"
        )
    else:
        response_text = "We couldn't identify your symptoms. Please consult a healthcare professional."

    return jsonify({"response": response_text})

if __name__ == "__main__":
    app.run(debug=True)

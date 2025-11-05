# New Diseases and Conditions Documentation

This document describes the new diseases and conditions that have been added to the Aushadham medical platform.

## Overview

Five new comprehensive questionnaire templates have been added to expand the platform's coverage of common and serious medical conditions:

1. **Cancer** - For cancer screening, suspicious symptoms, and support
2. **Diabetes** - For diabetes screening, management, and related symptoms
3. **Hypertension** - For high blood pressure monitoring and assessment
4. **Asthma** - For respiratory condition evaluation and management
5. **Arthritis** - For joint pain and arthritis-related concerns

## Implementation Details

### Cancer Questionnaire
- **Questions**: 13 comprehensive questions
- **Keywords**: cancer, tumor, tumour, malignancy, oncology, carcinoma, lump, mass
- **Focus Areas**:
  - Type of concern (screening, symptoms, diagnosed, family history)
  - Warning signs (unexplained weight loss, persistent fatigue, lumps)
  - Bleeding and changes in bodily functions
  - Family history and risk factors (tobacco use, age)
- **Conditional Questions**:
  - Lump location if unusual lumps detected
  - Family cancer type if family history positive
- **Recommendations**: Immediate medical attention, symptom tracking, screening tests
- **Key Message**: Professional oncologist evaluation required

### Diabetes Questionnaire
- **Questions**: 14 comprehensive questions
- **Keywords**: diabetes, diabetic, blood sugar, glucose, insulin, hyperglycemia
- **Focus Areas**:
  - Diagnosis status (Type 1, Type 2, pre-diabetic, concerned)
  - Classic symptoms (polydipsia, polyuria, polyphagia)
  - Complications (vision changes, slow healing, neuropathy)
  - Risk factors (BMI, family history, exercise habits)
  - Management (last blood sugar test)
- **Conditional Questions**:
  - Insulin regimen compliance for Type 1
  - Medication compliance for Type 2
- **Recommendations**: Blood glucose monitoring, diet management, exercise, regular check-ups
- **Medications**: Metformin, insulin, blood glucose meter

### Hypertension Questionnaire
- **Questions**: 14 comprehensive questions
- **Keywords**: hypertension, high blood pressure, blood pressure, bp
- **Focus Areas**:
  - Diagnosis status and recent readings
  - Symptoms (headaches, dizziness, chest pain)
  - Cardiovascular signs (palpitations, shortness of breath)
  - Risk factors (family history, salt intake, stress, alcohol)
  - Lifestyle factors (exercise habits)
- **Conditional Questions**:
  - Medication compliance for diagnosed patients
- **Recommendations**: Home BP monitoring, salt reduction, weight management, DASH diet, stress management
- **Medications**: ACE inhibitors/ARBs, diuretics, home BP monitor

### Asthma Questionnaire
- **Questions**: 14 comprehensive questions
- **Keywords**: asthma, wheezing, breathing difficulty, breathlessness
- **Focus Areas**:
  - Diagnosis status (childhood, adult-onset, suspected)
  - Symptoms (shortness of breath, wheezing, chest tightness, coughing)
  - Triggers (exercise, allergens, weather, stress)
  - Severity indicators (night symptoms, activity limitation)
  - Medication usage (rescue inhaler frequency)
  - Risk factors (family history, smoking exposure)
- **Conditional Questions**:
  - Current medication status for diagnosed patients
- **Recommendations**: Trigger avoidance, air quality management, medication compliance, asthma action plan
- **Medications**: Albuterol (rescue inhaler), inhaled corticosteroids, peak flow meter

### Arthritis Questionnaire
- **Questions**: 14 comprehensive questions
- **Keywords**: arthritis, joint pain, joint, rheumatoid, osteoarthritis
- **Focus Areas**:
  - Type of arthritis (osteoarthritis, rheumatoid, other, undiagnosed)
  - Symptoms (joint pain, stiffness, swelling)
  - Affected joints and patterns
  - Morning stiffness duration
  - Functional impact (range of motion, activity limitation)
  - Contributing factors (age, family history, weather sensitivity)
- **Conditional Questions**:
  - Pain intensity rating if joint pain present
- **Recommendations**: Low-impact exercise, weight management, heat/cold therapy, physical therapy
- **Medications**: Acetaminophen, NSAIDs, topical pain relievers

## Testing

All new questionnaires have been thoroughly tested:

### Unit Tests
- Template existence verification ✓
- Question loading ✓
- Questionnaire flow ✓
- Report generation ✓

### Integration Tests
- API endpoint functionality ✓
- Session management ✓
- Answer submission ✓
- Report generation with recommendations ✓

### Test Results
All 5 new disease questionnaires:
- Load correctly with proper number of questions
- Generate appropriate questions based on symptoms
- Calculate risk scores accurately
- Provide condition-specific recommendations
- Suggest appropriate medications and interventions
- Work seamlessly with existing API endpoints

## Usage Examples

### Starting a Cancer Questionnaire
```bash
curl -X POST http://localhost:5000/start_questionnaire \
  -H "Content-Type: application/json" \
  -d '{"symptom": "cancer", "description": "I found a lump and I am concerned"}'
```

### Starting a Diabetes Questionnaire
```bash
curl -X POST http://localhost:5000/start_questionnaire \
  -H "Content-Type: application/json" \
  -d '{"symptom": "diabetes", "description": "Increased thirst and frequent urination"}'
```

### Starting a Hypertension Questionnaire
```bash
curl -X POST http://localhost:5000/start_questionnaire \
  -H "Content-Type: application/json" \
  -d '{"symptom": "high blood pressure", "description": "Persistent headaches"}'
```

### Starting an Asthma Questionnaire
```bash
curl -X POST http://localhost:5000/start_questionnaire \
  -H "Content-Type: application/json" \
  -d '{"symptom": "asthma", "description": "Difficulty breathing and wheezing"}'
```

### Starting an Arthritis Questionnaire
```bash
curl -X POST http://localhost:5000/start_questionnaire \
  -H "Content-Type: application/json" \
  -d '{"symptom": "joint pain", "description": "Morning stiffness in my knees"}'
```

## Impact

These additions significantly expand the platform's medical coverage:

- **Previous coverage**: 4 conditions (stomach issues, headache, fever, cough)
- **New coverage**: 9 conditions (125% increase)
- **Total questions added**: 69 new comprehensive medical questions
- **Enhanced capability**: Now covers both acute symptoms and chronic conditions

The new questionnaires align with the platform's mission to:
- Bridge India's rural healthcare gap
- Enable AI-powered symptom assessment
- Reduce unnecessary clinic visits
- Ensure critical cases receive urgent attention
- Support early detection of serious conditions

## Medical Disclaimer

All questionnaires are designed for informational and triage purposes only. They do not replace professional medical advice, diagnosis, or treatment. Users are always advised to consult healthcare providers for proper evaluation and care, especially for serious conditions like cancer, diabetes, and uncontrolled hypertension.

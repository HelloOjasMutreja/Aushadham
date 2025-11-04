# Aushadham - Medical Healthcare Platform

## 🆕 New Features (v4.0)

The platform now includes a complete **user authentication system** with the ability to save questionnaire responses and provide feedback!

### New Features:
- ✅ **User Registration & Login** - Secure authentication with JWT tokens
- ✅ **Save Questionnaires** - Users can save their medical assessments to their profile
- ✅ **Feedback System** - Rate and provide feedback on questionnaires
- ✅ **User Profiles** - Manage personal information and view history
- ✅ **Secure Password Storage** - Bcrypt password hashing
- ✅ **Database Support** - SQLite, PostgreSQL, or MySQL

📖 **See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for complete API reference.**

## Available Backends

This project includes **two backend implementations**:

1. **Python Flask Backend** - Enhanced with authentication (`app.py`)
   - Run: `python app.py`
   - Requirements: `pip install -r requirements.txt`
   - Features: User authentication, database storage, JWT tokens

2. **Java Spring Boot Backend** - New implementation (`aushadham-backend/`)
   - Build: `cd aushadham-backend && mvn clean package`
   - Run: `java -jar target/aushadham-backend-1.0-SNAPSHOT.jar`

📖 **See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) for complete migration details.**

## Quick Start

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Optional: Create .env file for configuration
cp .env.example .env

# Run the application
python app.py
```

The API will be available at `http://localhost:5000`

### Testing
```bash
# Run the test suite
python test_api.py
```

---

**Sanjeevani Pro: Bridging India’s Rural Healthcare Gap with AI and Voice-Driven Triage**  

Sanjeevani Pro is a revolutionary healthcare platform designed to democratize access to quality medical care in India, with a laser focus on underserved rural populations. By integrating AI-powered symptom assessment, voice-based triage, and smart care coordination, the platform addresses systemic challenges such as acute doctor shortages, delayed diagnoses, and the near-absence of specialist care in remote regions. HealthAssist empowers patients to become the first point of contact in their healthcare journey, reducing unnecessary clinic visits, optimizing clinical efficiency, and ensuring critical cases receive urgent attention—all while lowering costs for patients and providers alike.  

### **Core Innovations**  
1. **AI-Driven First Appointment**:  
   - Patients input symptoms via a mobile app **or voice call**, triggering an adaptive questionnaire that mimics clinical reasoning. The AI model, trained on Indian health datasets, prioritizes region-specific conditions (e.g., tuberculosis, anemia) and generates a prioritized list of potential diagnoses with criticality scores.  
   - **Impact**: Reduces strain on overburdened doctors by resolving 30-40% of non-urgent cases at the triage stage.  

2. **Voice-Based Accessibility for Rural India**:  
   - **Toll-Free IVR System**: Patients without smartphones can call, authenticate via ABHA ID + OTP, and navigate the questionnaire using voice or keypad inputs. Speech-to-text engines tailored for Indian accents and regional languages ensure inclusivity.  
   - **Offline Coordination**: Post-assessment, lab referrals and appointment details are shared via SMS (with QR codes), bypassing internet dependency.  

3. **Specialist Shortage Mitigation**:  
   - The platform’s **Connection Algorithm** directs patients to the nearest available general physician or specialist, prioritizing severity and geographic proximity. Telemedicine integrations enable remote consultations for rare conditions.  
   - **Cost Efficiency**: Slashes travel expenses for rural patients and reduces “doctor-hopping” by 50% through accurate initial assessments.  

4. **Scalable Public Health Integration**:  
   - Partners with government initiatives like Ayushman Bharat and NIKSHAY (TB eradication) to identify disease outbreaks early. Aggregated anonymized data helps policymakers allocate resources to high-risk areas.  

### **Solving India’s Healthcare Challenges**  
- **Preventive Care**: Flags high-risk patients (e.g., diabetes, hypertension) for early intervention, reducing long-term costs.  
- **Reducing Misdiagnosis**: Standardized AI protocols minimize human error in rushed rural clinics.  
- **Empowering ASHA Workers**: Equips frontline workers with the platform to screen communities during outreach, with real-time doctor backup.  
- **ABHA Compliance**: Ensures seamless interoperability with India’s digital health ecosystem while adhering to DPDP Act (2023) standards.  

### **Vision**  
HealthAssist is not merely an app—it is a lifeline for millions trapped in healthcare deserts. By combining cutting-edge technology with grassroots accessibility, the platform bridges urban-rural disparities, transforms preventive care, and amplifies the impact of India’s limited medical workforce. For rural patients, it means timely, affordable, and dignified care. For doctors, it means focusing expertise where it matters most. For India, it means a healthier, more equitable future.  

**Tagline**: *“Where AI Meets Empathy: Healthcare for Every Bharat, Beyond Barriers.”*

![Sanjeevani_page-0001](https://github.com/user-attachments/assets/9afc4c87-faeb-4f9f-ac03-3de62f3a26f5)
![Sanjeevani_page-0002](https://github.com/user-attachments/assets/c246275b-6207-42a6-bac3-5a78370863c1)
![Sanjeevani_page-0003](https://github.com/user-attachments/assets/8831174d-23df-4ade-9ee2-787e95715ede)
![Sanjeevani_page-0004](https://github.com/user-attachments/assets/33e15021-960d-483e-a969-9df2fd537fbd)
![Sanjeevani_page-0005](https://github.com/user-attachments/assets/792215d7-580f-4970-8f93-bdad68dcc438)
![Sanjeevani_page-0006](https://github.com/user-attachments/assets/203b5f26-427b-49c8-908f-7cbb93b180f2)

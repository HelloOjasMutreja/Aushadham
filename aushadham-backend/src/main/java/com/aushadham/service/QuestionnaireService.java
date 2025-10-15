package com.aushadham.service;

import com.aushadham.config.QuestionnaireConfig;
import com.aushadham.dto.QuestionResponse;
import com.aushadham.model.*;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.concurrent.ConcurrentHashMap;
import java.util.stream.Collectors;

@Service
public class QuestionnaireService {

    private final Map<String, QuestionnaireSession> sessions = new ConcurrentHashMap<>();
    
    @Autowired
    private QuestionnaireConfig config;

    public Map<String, Object> startQuestionnaire(String symptom, String description) {
        String sessionId = UUID.randomUUID().toString();
        
        if (description == null || description.isEmpty()) {
            description = symptom;
        }
        
        QuestionnaireSession session = new QuestionnaireSession(sessionId, symptom, description);
        buildQuestions(session);
        sessions.put(sessionId, session);
        
        QuestionResponse question = getCurrentQuestion(session);
        
        Map<String, Object> response = new HashMap<>();
        response.put("sessionId", sessionId);
        response.put("message", "Starting questionnaire for: " + symptom);
        response.put("question", question);
        
        return response;
    }

    public Map<String, Object> submitAnswer(String sessionId, String answer, String action) {
        QuestionnaireSession session = sessions.get(sessionId);
        if (session == null) {
            throw new IllegalArgumentException("Invalid session");
        }

        if (!"previous".equals(action)) {
            submitAnswerToSession(session, answer);
        }

        boolean hasNext;
        switch (action) {
            case "next":
                hasNext = nextQuestion(session);
                break;
            case "previous":
                hasNext = previousQuestion(session);
                break;
            case "skip":
                hasNext = skipQuestion(session);
                break;
            default:
                hasNext = true;
        }

        Map<String, Object> response = new HashMap<>();
        response.put("completed", session.isCompleted());

        if (session.isCompleted()) {
            response.put("message", "Questionnaire completed!");
            response.put("sessionId", sessionId);
        } else {
            QuestionResponse question = getCurrentQuestion(session);
            response.put("question", question);
        }

        return response;
    }

    public QuestionResponse getCurrentQuestionResponse(String sessionId) {
        QuestionnaireSession session = sessions.get(sessionId);
        if (session == null) {
            throw new IllegalArgumentException("Invalid session");
        }
        return getCurrentQuestion(session);
    }

    public Report getReport(String sessionId) {
        QuestionnaireSession session = sessions.get(sessionId);
        if (session == null) {
            throw new IllegalArgumentException("Invalid session");
        }
        return generateReport(session);
    }

    private void buildQuestions(QuestionnaireSession session) {
        QuestionnaireTemplate template = getTemplate(session.getSymptom());
        if (template != null && template.getInitialQuestions() != null) {
            session.setQuestions(new ArrayList<>(template.getInitialQuestions()));
        }
    }

    private QuestionnaireTemplate getTemplate(String symptom) {
        String symptomLower = symptom.toLowerCase();
        
        String[] stomachKeywords = {"stomach", "belly", "abdomen", "tummy", "digestive", "gastric"};
        String[] headacheKeywords = {"head", "headache", "migraine", "temple"};
        String[] feverKeywords = {"fever", "temperature", "hot", "feverish"};
        String[] coughKeywords = {"cough", "coughing", "throat", "respiratory"};
        
        if (containsAny(symptomLower, stomachKeywords)) {
            return config.getStomachTemplate();
        } else if (containsAny(symptomLower, headacheKeywords)) {
            return config.getHeadacheTemplate();
        } else if (containsAny(symptomLower, feverKeywords)) {
            return config.getFeverTemplate();
        } else if (containsAny(symptomLower, coughKeywords)) {
            return config.getCoughTemplate();
        }
        
        return config.getStomachTemplate(); // Default
    }

    private boolean containsAny(String text, String[] keywords) {
        for (String keyword : keywords) {
            if (text.contains(keyword)) {
                return true;
            }
        }
        return false;
    }

    private QuestionResponse getCurrentQuestion(QuestionnaireSession session) {
        if (session.getCurrentIndex() < session.getQuestions().size()) {
            Question q = session.getQuestions().get(session.getCurrentIndex());
            
            QuestionResponse response = new QuestionResponse();
            response.setQuestion(q.getQuestion());
            response.setType(q.getType());
            response.setOptions(q.getOptions() != null ? q.getOptions() : Arrays.asList("Yes", "No"));
            response.setCurrent(session.getCurrentIndex() + 1);
            response.setTotal(session.getQuestions().size());
            response.setProgress(((session.getCurrentIndex() + 1) / (double) session.getQuestions().size()) * 100);
            
            return response;
        }
        return null;
    }

    private void submitAnswerToSession(QuestionnaireSession session, String answer) {
        if (session.getCurrentIndex() < session.getQuestions().size()) {
            String questionId = session.getQuestions().get(session.getCurrentIndex()).getId();
            session.getAnswers().put(questionId, answer);
            
            addConditionalQuestions(session, questionId, answer);
        }
    }

    private void addConditionalQuestions(QuestionnaireSession session, String questionId, String answer) {
        QuestionnaireTemplate template = getTemplate(session.getSymptom());
        if (template != null && template.getConditionalQuestions() != null) {
            Map<String, List<Question>> conditionals = template.getConditionalQuestions().get(questionId);
            if (conditionals != null && conditionals.containsKey(answer.toLowerCase())) {
                List<Question> newQuestions = conditionals.get(answer.toLowerCase());
                int insertIndex = session.getCurrentIndex() + 1;
                for (int i = 0; i < newQuestions.size(); i++) {
                    session.getQuestions().add(insertIndex + i, newQuestions.get(i));
                }
            }
        }
    }

    private boolean nextQuestion(QuestionnaireSession session) {
        if (session.getCurrentIndex() < session.getQuestions().size() - 1) {
            session.setCurrentIndex(session.getCurrentIndex() + 1);
            return true;
        } else {
            session.setCompleted(true);
            return false;
        }
    }

    private boolean previousQuestion(QuestionnaireSession session) {
        if (session.getCurrentIndex() > 0) {
            session.setCurrentIndex(session.getCurrentIndex() - 1);
            return true;
        }
        return false;
    }

    private boolean skipQuestion(QuestionnaireSession session) {
        if (session.getCurrentIndex() < session.getQuestions().size()) {
            String questionId = session.getQuestions().get(session.getCurrentIndex()).getId();
            session.getAnswers().put(questionId, "Skipped");
            return nextQuestion(session);
        }
        return false;
    }

    private Report generateReport(QuestionnaireSession session) {
        Report report = new Report();
        report.setSessionId(session.getSessionId());
        report.setSymptom(session.getSymptom());
        report.setInitialDescription(session.getInitialDescription());
        report.setAssessmentDate(LocalDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm")));
        
        long answeredCount = session.getAnswers().values().stream()
                .filter(a -> !"Skipped".equals(a))
                .count();
        report.setQuestionsAnswered((int) answeredCount);
        report.setTotalQuestions(session.getQuestions().size());
        
        int riskScore = calculateRiskScore(session);
        report.setRiskScore(riskScore);
        
        if (riskScore >= 15) {
            report.setSeverity("High");
            report.setUrgency("Seek immediate medical attention");
        } else if (riskScore >= 8) {
            report.setSeverity("Moderate");
            report.setUrgency("Consult a doctor within 24 hours");
        } else {
            report.setSeverity("Low");
            report.setUrgency("Monitor symptoms, see doctor if worsens");
        }
        
        generateRecommendations(report, session.getSymptom());
        
        report.setAnswers(session.getAnswers());
        
        List<Report.DetailedAnswer> detailedAnswers = new ArrayList<>();
        for (Question q : session.getQuestions()) {
            String answer = session.getAnswers().getOrDefault(q.getId(), "Not answered");
            detailedAnswers.add(new Report.DetailedAnswer(q.getQuestion(), answer, q.getWeight()));
        }
        report.setDetailedAnswers(detailedAnswers);
        
        report.setDisclaimer("This assessment is for informational purposes only and does not replace professional medical advice. Please consult a healthcare provider for proper diagnosis and treatment.");
        
        return report;
    }

    private int calculateRiskScore(QuestionnaireSession session) {
        int riskScore = 0;
        
        for (Question question : session.getQuestions()) {
            String answer = session.getAnswers().getOrDefault(question.getId(), "Not answered");
            String answerLower = answer.toLowerCase();
            String weight = question.getWeight();
            
            boolean isHighRisk = answerLower.contains("yes") || 
                                answerLower.contains("severe") || 
                                answerLower.contains("more than 3 days") ||
                                answerLower.contains("above 103") ||
                                answerLower.contains("7-9") ||
                                answerLower.contains("10");
            
            if (isHighRisk) {
                if ("high".equals(weight)) {
                    riskScore += 3;
                } else if ("medium".equals(weight)) {
                    riskScore += 2;
                } else {
                    riskScore += 1;
                }
            }
        }
        
        return riskScore;
    }

    private void generateRecommendations(Report report, String symptom) {
        String symptomLower = symptom.toLowerCase();
        
        if (symptomLower.contains("stomach") || symptomLower.contains("abdomen")) {
            report.setRecommendations(Arrays.asList(
                "Stay hydrated with small sips of water",
                "Eat bland foods (BRAT diet: Bananas, Rice, Applesauce, Toast)",
                "Avoid dairy, caffeine, and fatty foods",
                "Rest and avoid strenuous activities"
            ));
            report.setSuggestedMedications(Arrays.asList(
                new Medication("Antacids (Tums, Mylanta)", "For acid reflux or indigestion"),
                new Medication("Bismuth subsalicylate (Pepto-Bismol)", "For general stomach upset"),
                new Medication("Simethicone (Gas-X)", "For gas and bloating")
            ));
        } else if (symptomLower.contains("head")) {
            report.setRecommendations(Arrays.asList(
                "Rest in a quiet, dark room",
                "Apply cold compress to forehead",
                "Stay hydrated",
                "Practice relaxation techniques",
                "Maintain regular sleep schedule"
            ));
            report.setSuggestedMedications(Arrays.asList(
                new Medication("Acetaminophen (Tylenol)", "For mild to moderate pain"),
                new Medication("Ibuprofen (Advil, Motrin)", "For inflammation and pain"),
                new Medication("Aspirin", "For tension headaches")
            ));
        } else if (symptomLower.contains("fever")) {
            report.setRecommendations(Arrays.asList(
                "Rest and get plenty of sleep",
                "Stay hydrated with water and electrolyte drinks",
                "Use cool compresses",
                "Wear light clothing",
                "Monitor temperature regularly"
            ));
            report.setSuggestedMedications(Arrays.asList(
                new Medication("Acetaminophen (Tylenol)", "To reduce fever"),
                new Medication("Ibuprofen (Advil, Motrin)", "To reduce fever and body aches")
            ));
        } else if (symptomLower.contains("cough")) {
            report.setRecommendations(Arrays.asList(
                "Stay hydrated to thin mucus",
                "Use a humidifier",
                "Gargle with warm salt water",
                "Avoid irritants like smoke",
                "Elevate head while sleeping"
            ));
            report.setSuggestedMedications(Arrays.asList(
                new Medication("Dextromethorphan (Robitussin)", "For dry cough"),
                new Medication("Guaifenesin (Mucinex)", "For productive cough"),
                new Medication("Throat lozenges", "For throat irritation")
            ));
        }
    }

    public Map<String, Object> getHealthCheck() {
        Map<String, Object> health = new HashMap<>();
        health.put("status", "healthy");
        health.put("activeSessions", sessions.size());
        health.put("timestamp", LocalDateTime.now().toString());
        return health;
    }
}

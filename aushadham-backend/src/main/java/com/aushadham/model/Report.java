package com.aushadham.model;

import java.util.List;
import java.util.Map;

public class Report {
    private String sessionId;
    private String symptom;
    private String initialDescription;
    private String assessmentDate;
    private int questionsAnswered;
    private int totalQuestions;
    private String severity;
    private String urgency;
    private int riskScore;
    private List<String> recommendations;
    private List<Medication> suggestedMedications;
    private Map<String, String> answers;
    private List<DetailedAnswer> detailedAnswers;
    private String disclaimer;

    public Report() {
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getSymptom() {
        return symptom;
    }

    public void setSymptom(String symptom) {
        this.symptom = symptom;
    }

    public String getInitialDescription() {
        return initialDescription;
    }

    public void setInitialDescription(String initialDescription) {
        this.initialDescription = initialDescription;
    }

    public String getAssessmentDate() {
        return assessmentDate;
    }

    public void setAssessmentDate(String assessmentDate) {
        this.assessmentDate = assessmentDate;
    }

    public int getQuestionsAnswered() {
        return questionsAnswered;
    }

    public void setQuestionsAnswered(int questionsAnswered) {
        this.questionsAnswered = questionsAnswered;
    }

    public int getTotalQuestions() {
        return totalQuestions;
    }

    public void setTotalQuestions(int totalQuestions) {
        this.totalQuestions = totalQuestions;
    }

    public String getSeverity() {
        return severity;
    }

    public void setSeverity(String severity) {
        this.severity = severity;
    }

    public String getUrgency() {
        return urgency;
    }

    public void setUrgency(String urgency) {
        this.urgency = urgency;
    }

    public int getRiskScore() {
        return riskScore;
    }

    public void setRiskScore(int riskScore) {
        this.riskScore = riskScore;
    }

    public List<String> getRecommendations() {
        return recommendations;
    }

    public void setRecommendations(List<String> recommendations) {
        this.recommendations = recommendations;
    }

    public List<Medication> getSuggestedMedications() {
        return suggestedMedications;
    }

    public void setSuggestedMedications(List<Medication> suggestedMedications) {
        this.suggestedMedications = suggestedMedications;
    }

    public Map<String, String> getAnswers() {
        return answers;
    }

    public void setAnswers(Map<String, String> answers) {
        this.answers = answers;
    }

    public List<DetailedAnswer> getDetailedAnswers() {
        return detailedAnswers;
    }

    public void setDetailedAnswers(List<DetailedAnswer> detailedAnswers) {
        this.detailedAnswers = detailedAnswers;
    }

    public String getDisclaimer() {
        return disclaimer;
    }

    public void setDisclaimer(String disclaimer) {
        this.disclaimer = disclaimer;
    }

    public static class DetailedAnswer {
        private String question;
        private String answer;
        private String importance;

        public DetailedAnswer() {
        }

        public DetailedAnswer(String question, String answer, String importance) {
            this.question = question;
            this.answer = answer;
            this.importance = importance;
        }

        public String getQuestion() {
            return question;
        }

        public void setQuestion(String question) {
            this.question = question;
        }

        public String getAnswer() {
            return answer;
        }

        public void setAnswer(String answer) {
            this.answer = answer;
        }

        public String getImportance() {
            return importance;
        }

        public void setImportance(String importance) {
            this.importance = importance;
        }
    }
}

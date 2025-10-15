package com.aushadham.model;

import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class QuestionnaireSession {
    private String sessionId;
    private String symptom;
    private String initialDescription;
    private List<Question> questions;
    private int currentIndex;
    private Map<String, String> answers;
    private boolean completed;
    private LocalDateTime startTime;

    public QuestionnaireSession() {
        this.questions = new ArrayList<>();
        this.answers = new HashMap<>();
        this.currentIndex = 0;
        this.completed = false;
        this.startTime = LocalDateTime.now();
    }

    public QuestionnaireSession(String sessionId, String symptom, String initialDescription) {
        this();
        this.sessionId = sessionId;
        this.symptom = symptom;
        this.initialDescription = initialDescription;
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

    public List<Question> getQuestions() {
        return questions;
    }

    public void setQuestions(List<Question> questions) {
        this.questions = questions;
    }

    public int getCurrentIndex() {
        return currentIndex;
    }

    public void setCurrentIndex(int currentIndex) {
        this.currentIndex = currentIndex;
    }

    public Map<String, String> getAnswers() {
        return answers;
    }

    public void setAnswers(Map<String, String> answers) {
        this.answers = answers;
    }

    public boolean isCompleted() {
        return completed;
    }

    public void setCompleted(boolean completed) {
        this.completed = completed;
    }

    public LocalDateTime getStartTime() {
        return startTime;
    }

    public void setStartTime(LocalDateTime startTime) {
        this.startTime = startTime;
    }
}

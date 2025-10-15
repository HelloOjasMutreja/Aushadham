package com.aushadham.dto;

public class StartQuestionnaireRequest {
    private String symptom;
    private String description;

    public StartQuestionnaireRequest() {
    }

    public String getSymptom() {
        return symptom;
    }

    public void setSymptom(String symptom) {
        this.symptom = symptom;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }
}

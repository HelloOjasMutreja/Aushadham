package com.aushadham.model;

import java.util.List;
import java.util.Map;

public class QuestionnaireTemplate {
    private List<Question> initialQuestions;
    private Map<String, Map<String, List<Question>>> conditionalQuestions;

    public QuestionnaireTemplate() {
    }

    public QuestionnaireTemplate(List<Question> initialQuestions, 
                                Map<String, Map<String, List<Question>>> conditionalQuestions) {
        this.initialQuestions = initialQuestions;
        this.conditionalQuestions = conditionalQuestions;
    }

    public List<Question> getInitialQuestions() {
        return initialQuestions;
    }

    public void setInitialQuestions(List<Question> initialQuestions) {
        this.initialQuestions = initialQuestions;
    }

    public Map<String, Map<String, List<Question>>> getConditionalQuestions() {
        return conditionalQuestions;
    }

    public void setConditionalQuestions(Map<String, Map<String, List<Question>>> conditionalQuestions) {
        this.conditionalQuestions = conditionalQuestions;
    }
}

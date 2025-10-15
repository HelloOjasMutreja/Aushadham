package com.aushadham.model;

import java.util.List;

public class Question {
    private String id;
    private String question;
    private String type;
    private List<String> options;
    private String weight;

    public Question() {
    }

    public Question(String id, String question, String type, List<String> options, String weight) {
        this.id = id;
        this.question = question;
        this.type = type;
        this.options = options;
        this.weight = weight;
    }

    public String getId() {
        return id;
    }

    public void setId(String id) {
        this.id = id;
    }

    public String getQuestion() {
        return question;
    }

    public void setQuestion(String question) {
        this.question = question;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public List<String> getOptions() {
        return options;
    }

    public void setOptions(List<String> options) {
        this.options = options;
    }

    public String getWeight() {
        return weight;
    }

    public void setWeight(String weight) {
        this.weight = weight;
    }
}

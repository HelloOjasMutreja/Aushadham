package com.aushadham.dto;

public class SubmitAnswerRequest {
    private String sessionId;
    private String answer;
    private String action; // next, previous, skip

    public SubmitAnswerRequest() {
    }

    public String getSessionId() {
        return sessionId;
    }

    public void setSessionId(String sessionId) {
        this.sessionId = sessionId;
    }

    public String getAnswer() {
        return answer;
    }

    public void setAnswer(String answer) {
        this.answer = answer;
    }

    public String getAction() {
        return action != null ? action : "next";
    }

    public void setAction(String action) {
        this.action = action;
    }
}

package com.aushadham.model;

public class Medication {
    private String name;
    private String purpose;

    public Medication() {
    }

    public Medication(String name, String purpose) {
        this.name = name;
        this.purpose = purpose;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getPurpose() {
        return purpose;
    }

    public void setPurpose(String purpose) {
        this.purpose = purpose;
    }
}

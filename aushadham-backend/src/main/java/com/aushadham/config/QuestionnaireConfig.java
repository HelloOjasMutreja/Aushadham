package com.aushadham.config;

import com.aushadham.model.Question;
import com.aushadham.model.QuestionnaireTemplate;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

import java.util.*;

@Configuration
public class QuestionnaireConfig {

    public QuestionnaireTemplate getStomachTemplate() {
        List<Question> initialQuestions = Arrays.asList(
            new Question("hydration", "Did you drink enough water today (at least 6-8 glasses)?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("recent_meal", "Did you eat anything unusual or outside food in the last 24 hours?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("pain_location", "Is the pain in your upper abdomen or lower abdomen?", 
                "choice", Arrays.asList("Upper abdomen", "Lower abdomen", "All over", "Around belly button"), "high"),
            new Question("pain_type", "How would you describe the pain?", 
                "choice", Arrays.asList("Sharp/Stabbing", "Dull/Aching", "Cramping", "Burning"), "medium"),
            new Question("nausea", "Are you experiencing nausea or have you vomited?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("bowel_movement", "Have you had normal bowel movements today?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("fever", "Do you have a fever or feel feverish?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("exercise", "Were you involved in any strenuous exercise in the last couple of days?", 
                "yes_no", Arrays.asList("Yes", "No"), "low"),
            new Question("stress", "Have you been under unusual stress lately?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("medication", "Have you taken any medication for this pain?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("duration", "How long have you been experiencing this pain?", 
                "choice", Arrays.asList("Less than 1 hour", "1-3 hours", "3-6 hours", "More than 6 hours"), "high"),
            new Question("severity", "On a scale of 1-10, how severe is your pain?", 
                "scale", Arrays.asList("1-3 (Mild)", "4-6 (Moderate)", "7-9 (Severe)", "10 (Unbearable)"), "high")
        );

        Map<String, Map<String, List<Question>>> conditionalQuestions = new HashMap<>();
        
        Map<String, List<Question>> nauseaConditionals = new HashMap<>();
        nauseaConditionals.put("yes", Arrays.asList(
            new Question("vomit_frequency", "How many times have you vomited?", 
                "choice", Arrays.asList("Once", "2-3 times", "More than 3 times", "Just nauseous, no vomiting"), "high")
        ));
        conditionalQuestions.put("nausea", nauseaConditionals);
        
        Map<String, List<Question>> mealConditionals = new HashMap<>();
        mealConditionals.put("yes", Arrays.asList(
            new Question("food_type", "What type of food did you eat?", 
                "choice", Arrays.asList("Street food", "Restaurant food", "Home-cooked but unusual", "Dairy products"), "medium")
        ));
        conditionalQuestions.put("recent_meal", mealConditionals);

        return new QuestionnaireTemplate(initialQuestions, conditionalQuestions);
    }

    public QuestionnaireTemplate getHeadacheTemplate() {
        List<Question> initialQuestions = Arrays.asList(
            new Question("location", "Where exactly is your headache located?", 
                "choice", Arrays.asList("Forehead", "Temples", "Back of head", "One side only", "Entire head"), "high"),
            new Question("pain_type", "How would you describe the pain?", 
                "choice", Arrays.asList("Throbbing/Pulsating", "Constant pressure", "Sharp/Stabbing", "Dull ache"), "high"),
            new Question("triggers", "Did anything specific trigger this headache?", 
                "choice", Arrays.asList("Stress", "Lack of sleep", "Bright lights", "Loud noise", "Not sure"), "medium"),
            new Question("light_sensitivity", "Are you sensitive to light right now?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("sound_sensitivity", "Are you sensitive to sound right now?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("nausea", "Do you feel nauseous?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("vision", "Are you experiencing any vision changes (blurriness, spots, auras)?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("frequency", "How often do you get headaches?", 
                "choice", Arrays.asList("Rarely", "Once a month", "Weekly", "Daily"), "medium"),
            new Question("hydration", "Have you been drinking enough water today?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("sleep", "How many hours did you sleep last night?", 
                "choice", Arrays.asList("Less than 4", "4-6 hours", "6-8 hours", "More than 8"), "medium"),
            new Question("screen_time", "Have you been looking at screens for extended periods today?", 
                "yes_no", Arrays.asList("Yes", "No"), "low"),
            new Question("medication", "Have you taken any pain medication?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium")
        );

        Map<String, Map<String, List<Question>>> conditionalQuestions = new HashMap<>();
        
        Map<String, List<Question>> medicationConditionals = new HashMap<>();
        medicationConditionals.put("yes", Arrays.asList(
            new Question("med_effect", "Did the medication help?", 
                "choice", Arrays.asList("Yes, completely", "Partially", "Not at all", "Made it worse"), "high")
        ));
        conditionalQuestions.put("medication", medicationConditionals);

        return new QuestionnaireTemplate(initialQuestions, conditionalQuestions);
    }

    public QuestionnaireTemplate getFeverTemplate() {
        List<Question> initialQuestions = Arrays.asList(
            new Question("temperature", "What is your current temperature?", 
                "choice", Arrays.asList("98-99°F", "100-101°F", "102-103°F", "Above 103°F", "Don't know"), "high"),
            new Question("duration", "How long have you had this fever?", 
                "choice", Arrays.asList("Just started", "Few hours", "1 day", "2-3 days", "More than 3 days"), "high"),
            new Question("chills", "Are you experiencing chills or shivering?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("sweating", "Are you sweating excessively?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("body_ache", "Do you have body aches or muscle pain?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("throat", "Do you have a sore throat?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("cough", "Do you have a cough?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("appetite", "Have you lost your appetite?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("fatigue", "Are you feeling unusually tired or weak?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("exposure", "Have you been exposed to anyone who was sick recently?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium")
        );

        Map<String, Map<String, List<Question>>> conditionalQuestions = new HashMap<>();
        
        Map<String, List<Question>> coughConditionals = new HashMap<>();
        coughConditionals.put("yes", Arrays.asList(
            new Question("cough_type", "Is your cough dry or producing phlegm?", 
                "choice", Arrays.asList("Dry cough", "With phlegm", "Both"), "high")
        ));
        conditionalQuestions.put("cough", coughConditionals);

        return new QuestionnaireTemplate(initialQuestions, conditionalQuestions);
    }

    public QuestionnaireTemplate getCoughTemplate() {
        List<Question> initialQuestions = Arrays.asList(
            new Question("cough_type", "Is your cough dry or producing phlegm/mucus?", 
                "choice", Arrays.asList("Dry cough", "With clear phlegm", "With colored phlegm", "With blood"), "high"),
            new Question("duration", "How long have you been coughing?", 
                "choice", Arrays.asList("Just started", "2-3 days", "1 week", "2 weeks", "More than 2 weeks"), "high"),
            new Question("frequency", "How often are you coughing?", 
                "choice", Arrays.asList("Occasionally", "Frequently", "Constant", "Only at night", "Only in morning"), "medium"),
            new Question("chest_pain", "Do you have chest pain when coughing?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("breathing", "Are you experiencing shortness of breath?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("wheezing", "Do you hear wheezing when breathing?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("fever", "Do you have a fever?", 
                "yes_no", Arrays.asList("Yes", "No"), "high"),
            new Question("smoking", "Do you smoke or have you been exposed to smoke?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("allergies", "Do you have known allergies?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium"),
            new Question("environment", "Have you been exposed to dust, chemicals, or irritants?", 
                "yes_no", Arrays.asList("Yes", "No"), "medium")
        );

        Map<String, Map<String, List<Question>>> conditionalQuestions = new HashMap<>();

        return new QuestionnaireTemplate(initialQuestions, conditionalQuestions);
    }
}

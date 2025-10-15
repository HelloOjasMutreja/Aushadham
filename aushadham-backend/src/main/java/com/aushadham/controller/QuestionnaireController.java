package com.aushadham.controller;

import com.aushadham.dto.*;
import com.aushadham.model.Report;
import com.aushadham.service.QuestionnaireService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/")
public class QuestionnaireController {

    @Autowired
    private QuestionnaireService questionnaireService;

    @GetMapping
    public ResponseEntity<Map<String, Object>> home() {
        Map<String, Object> response = new HashMap<>();
        response.put("status", "Medical Questionnaire API is running!");
        response.put("version", "3.0");
        response.put("endpoints", new String[]{
            "/start_questionnaire",
            "/submit_answer",
            "/next_question",
            "/previous_question",
            "/skip_question",
            "/get_current_question",
            "/get_report"
        });
        return ResponseEntity.ok(response);
    }

    @PostMapping("/start_questionnaire")
    public ResponseEntity<ApiResponse<Map<String, Object>>> startQuestionnaire(
            @RequestBody StartQuestionnaireRequest request) {
        try {
            Map<String, Object> result = questionnaireService.startQuestionnaire(
                request.getSymptom() != null ? request.getSymptom() : "",
                request.getDescription()
            );
            return ResponseEntity.ok(ApiResponse.success(result));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/submit_answer")
    public ResponseEntity<ApiResponse<Map<String, Object>>> submitAnswer(
            @RequestBody SubmitAnswerRequest request) {
        try {
            Map<String, Object> result = questionnaireService.submitAnswer(
                request.getSessionId(),
                request.getAnswer(),
                request.getAction()
            );
            return ResponseEntity.ok(ApiResponse.success(result));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/get_current_question")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getCurrentQuestion(
            @RequestBody SessionRequest request) {
        try {
            QuestionResponse question = questionnaireService.getCurrentQuestionResponse(
                request.getSessionId()
            );
            
            Map<String, Object> result = new HashMap<>();
            result.put("question", question);
            result.put("completed", false);
            
            return ResponseEntity.ok(ApiResponse.success(result));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(e.getMessage()));
        }
    }

    @PostMapping("/get_report")
    public ResponseEntity<ApiResponse<Map<String, Object>>> getReport(
            @RequestBody SessionRequest request) {
        try {
            Report report = questionnaireService.getReport(request.getSessionId());
            
            Map<String, Object> result = new HashMap<>();
            result.put("report", report);
            
            return ResponseEntity.ok(ApiResponse.success(result));
        } catch (IllegalArgumentException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                .body(ApiResponse.error(e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                .body(ApiResponse.error(e.getMessage()));
        }
    }

    @GetMapping("/health_check")
    public ResponseEntity<Map<String, Object>> healthCheck() {
        return ResponseEntity.ok(questionnaireService.getHealthCheck());
    }
}

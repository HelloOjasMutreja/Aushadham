# Aushadham Backend - Java Spring Boot

Medical Questionnaire Backend implemented in Java Spring Boot.

## Prerequisites

- Java 17 or higher
- Maven 3.6+

## Building the Project

```bash
cd aushadham-backend
mvn clean package
```

## Running the Application

```bash
java -jar target/aushadham-backend-1.0-SNAPSHOT.jar
```

The application will start on port 5000.

## API Endpoints

- `GET /` - API information
- `POST /start_questionnaire` - Start a new questionnaire
- `POST /submit_answer` - Submit an answer to the current question
- `POST /get_current_question` - Get the current question
- `POST /get_report` - Get the final report
- `GET /health_check` - Health check endpoint

## Example Usage

### Start Questionnaire
```bash
curl -X POST http://localhost:5000/start_questionnaire \
  -H "Content-Type: application/json" \
  -d '{"symptom":"headache","description":"I have a severe headache"}'
```

### Submit Answer
```bash
curl -X POST http://localhost:5000/submit_answer \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"YOUR_SESSION_ID","answer":"Forehead","action":"next"}'
```

### Get Report
```bash
curl -X POST http://localhost:5000/get_report \
  -H "Content-Type: application/json" \
  -d '{"sessionId":"YOUR_SESSION_ID"}'
```

## Testing

Run tests with:
```bash
mvn test
```

## Project Structure

```
src/
├── main/
│   ├── java/com/aushadham/
│   │   ├── App.java                  # Main Spring Boot application
│   │   ├── config/                   # Configuration classes
│   │   ├── controller/               # REST controllers
│   │   ├── dto/                      # Data Transfer Objects
│   │   ├── model/                    # Domain models
│   │   └── service/                  # Business logic
│   └── resources/
│       └── application.properties    # Application configuration
└── test/
    └── java/com/aushadham/           # Test classes
```

# Migration Guide: Python Flask to Java Spring Boot

This document describes the migration from the Python Flask backend to the Java Spring Boot backend.

## Overview

The original Python Flask application (`app.py`) has been fully converted to a Java Spring Boot application located in the `aushadham-backend` directory.

## What Was Converted

### 1. Core Application
- **Python Flask** → **Java Spring Boot 3.1.5**
- Port: 5000 (unchanged)
- All REST endpoints maintained
- Session management using `ConcurrentHashMap`

### 2. Project Structure

**Original Python:**
```
app.py
requirements.txt
```

**New Java:**
```
aushadham-backend/
├── pom.xml                           # Maven configuration
├── src/
│   ├── main/
│   │   ├── java/com/aushadham/
│   │   │   ├── App.java              # Main application
│   │   │   ├── config/               # CORS and questionnaire templates
│   │   │   ├── controller/           # REST API endpoints
│   │   │   ├── dto/                  # Request/Response objects
│   │   │   ├── model/                # Domain models
│   │   │   └── service/              # Business logic
│   │   └── resources/
│   │       └── application.properties
│   └── test/
│       └── java/com/aushadham/       # Unit tests
└── README.md
```

### 3. API Endpoints

All endpoints from the Flask application have been replicated:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/start_questionnaire` | POST | Start new questionnaire |
| `/submit_answer` | POST | Submit answer and navigate |
| `/get_current_question` | POST | Get current question |
| `/get_report` | POST | Generate final report |
| `/health_check` | GET | Health status |

### 4. Features Preserved

✅ All questionnaire templates (stomach, headache, fever, cough)  
✅ Conditional question logic  
✅ Risk score calculation  
✅ Report generation with recommendations  
✅ Session management  
✅ CORS support  
✅ Medical recommendations and medications  

## Key Differences

### Session Management
- **Python:** In-memory dictionary
- **Java:** ConcurrentHashMap for thread-safety

### Type System
- **Python:** Dynamic typing
- **Java:** Static typing with model classes

### Dependency Management
- **Python:** requirements.txt with pip
- **Java:** pom.xml with Maven

## Running the Java Backend

### Build
```bash
cd aushadham-backend
mvn clean package
```

### Run
```bash
java -jar target/aushadham-backend-1.0-SNAPSHOT.jar
```

Or use Maven:
```bash
mvn spring-boot:run
```

## Testing

The Java backend has been tested to ensure:
1. All endpoints work correctly
2. Question flow matches Python version
3. Conditional questions trigger properly
4. Report generation produces same structure
5. Session management is thread-safe
6. No security vulnerabilities (CodeQL verified)

## API Compatibility

The Java backend maintains **100% API compatibility** with the Python version. The frontend HTML file (`index.html`) works with both backends without any modifications.

Simply change the `API_BASE_URL` in `index.html` to point to the Java backend:
```javascript
const API_BASE_URL = 'http://localhost:5000';  // Java backend
```

## Benefits of Java Spring Boot

1. **Type Safety:** Compile-time type checking prevents runtime errors
2. **Performance:** Better performance for concurrent requests
3. **Scalability:** Built-in support for enterprise features
4. **Maintenance:** Strongly typed code is easier to maintain
5. **Security:** CodeQL analysis shows zero vulnerabilities
6. **Testing:** Comprehensive test framework with JUnit 5
7. **Deployment:** Single JAR file for easy deployment

## Next Steps

### For Development
1. Run the Java backend instead of Python
2. Keep the existing HTML frontend unchanged
3. Use the same API endpoints

### For Production
1. Build the JAR file: `mvn clean package`
2. Deploy the JAR to your server
3. Run with: `java -jar aushadham-backend-1.0-SNAPSHOT.jar`
4. Configure environment variables if needed

## Environment Variables

The Java backend can be configured using standard Spring Boot properties:

```bash
# Change port
java -jar aushadham-backend-1.0-SNAPSHOT.jar --server.port=8080

# Set profile
java -jar aushadham-backend-1.0-SNAPSHOT.jar --spring.profiles.active=prod
```

## Support

For any issues with the Java backend:
1. Check the README in `aushadham-backend/`
2. Review the API documentation
3. Run the test suite: `mvn test`
4. Check application logs for errors

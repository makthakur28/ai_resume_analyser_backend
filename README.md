# AI Resume Analyzer Backend

This is a production-ready, highly modular, and scalable backend API for an AI Resume Analyzer platform. Built with FastAPI, Docker, and the Groq LLM API.

## Architecture

The project strictly follows a layered Clean Architecture pattern to ensure high modularity, easy testing, and scalability:

*   **`api/`**: Contains the routing logic and endpoint definitions. Separated by API versions (e.g., `v1`).
*   **`core/`**: Core application logic and setup, such as structured logging configuration.
*   **`config/`**: Centralized configuration management using Pydantic Settings, pulling from environment variables.
*   **`services/`**: The main business logic layer. Coordinates between different components (e.g., orchestrating text extraction and LLM calls).
*   **`integrations/`**: Contains external service clients, isolating the application from third-party vendor changes (e.g., Groq API client).
*   **`schemas/`**: Pydantic models for strict request/response validation.
*   **`exceptions/`**: Centralized custom application exceptions and error handlers.
*   **`middleware/`**: Request/Response interceptors, like logging or future authentication layers.
*   **`dependencies/`**: FastAPI dependency injection providers, ensuring loosely coupled components.
*   **`prompts/`**: Centralized location for LLM prompt engineering, isolating prompt tuning from business logic.

### Scalability Details

Designed as the foundation for a heavily funded AI SaaS:
1.  **Asynchronous By Default**: Utilizes `async/await` extensively (FastAPI, AsyncGroq client) ensuring non-blocking operations capable of handling thousands of concurrent requests.
2.  **Dependency Injection**: Facilitates easy swapping of components (e.g., replacing Groq with OpenAI or switching PDF parsers) and simplifies unit testing via mocking.
3.  **Stateless Design**: Completely stateless container ready for horizontal scaling behind a load balancer (e.g., Kubernetes Ingress or AWS ALB).
4.  **Future-Ready Structure**: The folder layout easily accommodates future additions like `repositories/` (for DB access), `models/` (SQLAlchemy ORM models), and background task workers (Celery/RabbitMQ) without needing a massive refactor.

## Environment Setup

1.  Copy the example environment variables file:
    ```bash
    cp .env.example .env
    ```
2.  Update the `.env` file with your actual `GROQ_API_KEY`.

## Startup Instructions

### Using Docker (Recommended for Production/Deployment)

1.  Build and run the containers using Docker Compose:
    ```bash
    docker-compose up --build -d
    ```
2.  To view logs:
    ```bash
    docker-compose logs -f
    ```

### Local Development (Virtual Environment)

1.  Create and activate a virtual environment:
    ```bash
    python3.11 -m venv venv
    source venv/bin/activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the server:
    ```bash
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    ```

## API Documentation

Once the server is running, FastAPI automatically generates interactive documentation:
*   **Swagger UI**: [http://localhost:8000/api/docs](http://localhost:8000/api/docs)
*   **ReDoc**: [http://localhost:8000/api/redoc](http://localhost:8000/api/redoc)

### Key Endpoints

*   **`GET /api/v1/health/`**: Basic health check to ensure the application is up and running.
*   **`POST /api/v1/resume/analyze`**: 
    *   **Input**: Requires a `multipart/form-data` upload containing a PDF file (key: `file`).
    *   **Output**: Returns a strict JSON response adhering to the `ResumeAnalysisResponse` schema containing the ATS score, strengths, weaknesses, suggested improvements, and more.

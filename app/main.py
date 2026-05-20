from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import settings
from app.api.v1.router import api_router
from app.middleware.logging_middleware import LoggingMiddleware
from app.middleware.error_handler import setup_exception_handlers
from app.core.logging import setup_logging

def create_app() -> FastAPI:
    # Set up basic structured logging
    setup_logging(settings.LOG_LEVEL)

    # Initialize FastAPI App
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        description="A scalable AI backend for resume analysis using Groq.",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # For production, this should be restricted
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add custom middlewares
    app.add_middleware(LoggingMiddleware)

    # Configure exception handlers
    setup_exception_handlers(app)

    # Include API Router
    app.include_router(api_router, prefix="/api/v1")

    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

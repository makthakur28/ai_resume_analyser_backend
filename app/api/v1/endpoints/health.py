from fastapi import APIRouter
from app.schemas.health import HealthCheckResponse
from app.config.settings import settings

router = APIRouter()

@router.get("/", response_model=HealthCheckResponse)
async def health_check():
    """
    Check the health and environment of the API.
    """
    return HealthCheckResponse(
        status="ok",
        version=settings.VERSION,
        environment=settings.ENVIRONMENT
    )

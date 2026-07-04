import logging

from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.resume import router as resume_router
from app.core.config import get_settings
from app.core.logging import configure_logging

settings = get_settings()
configure_logging(settings)

logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(health_router)
app.include_router(resume_router)

logger.info("FastAPI application configured")

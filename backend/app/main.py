from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# The obsolete 'items' router has been removed.
from app.api.routes import login, private, users, utils
from app.core.config import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware - always add it, but configure origins based on environment
cors_origins = []

# Add BACKEND_CORS_ORIGINS if set
if settings.BACKEND_CORS_ORIGINS:
    cors_origins.extend([str(origin) for origin in settings.BACKEND_CORS_ORIGINS])

# Add FRONTEND_HOST to allowed origins
if settings.FRONTEND_HOST:
    cors_origins.append(settings.FRONTEND_HOST)

# For production, ensure we have the specific origins
if settings.ENVIRONMENT != "local":
    production_origins = [
        "https://troycourselab.netlify.app",
        "https://troycourselab.up.railway.app",
    ]
    for origin in production_origins:
        if origin not in cors_origins:
            cors_origins.append(origin)

logger.info(f"CORS Origins: {cors_origins}")
logger.info(f"Environment: {settings.ENVIRONMENT}")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
)

api_router = APIRouter()

# Include only the necessary and active routers for the application.
api_router.include_router(login.router, prefix="/api/v1")
api_router.include_router(users.router, prefix="/api/v1")
api_router.include_router(utils.router, prefix="/api/v1")

# Conditionally include the 'private' router for local development environments.
if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router, prefix="/api/v1")

# Include the API router in the main app
app.include_router(api_router)

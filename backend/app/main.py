from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

# The obsolete 'items' router has been removed.
from app.api.routes import login, private, users, utils
from app.core.config import settings

# Create the FastAPI app instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
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

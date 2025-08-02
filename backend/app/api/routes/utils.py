from fastapi import APIRouter, Depends
from app.core.config import settings
from app.core.security import get_current_active_superuser
from app.schemas import Message
from pydantic import EmailStr

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    from app.email_service import send_email

    send_email(
        email_to=email_to,
        subject="Test email",
        template_name="test_email.html",
    )

    return Message(message="Test email sent")


@router.get("/health-check/")
async def health_check() -> bool:
    return True


@router.get("/debug/cors/")
async def debug_cors() -> dict:
    """Debug endpoint to check CORS configuration"""
    return {
        "BACKEND_CORS_ORIGINS": settings.BACKEND_CORS_ORIGINS,
        "all_cors_origins": settings.all_cors_origins,
        "FRONTEND_HOST": settings.FRONTEND_HOST,
        "ENVIRONMENT": settings.ENVIRONMENT,
    }

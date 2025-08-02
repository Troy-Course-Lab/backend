from fastapi import APIRouter, HTTPException, Depends

from app import crud
from app.api.deps import SessionDep
from app.schemas import Message, UserCreate
from app.core.config import settings
from app.utils import send_new_account_email
from app.core.security import generate_email_verification_token, verify_email_verification_token

router = APIRouter()


@router.post("/register", response_model=Message, status_code=201)
def register_new_user(session: SessionDep, user_in: UserCreate) -> Message:
    """
    Create new user, validating email and triggering verification email.
    """
    if not user_in.email.endswith("@troy.edu"):
        raise HTTPException(
            status_code=400,
            detail="Registration is only allowed with a @troy.edu email address.",
        )

    user = crud.get_user_by_email(session=session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = crud.create_user(session=session, user_in=user_in)

    if settings.EMAILS_ENABLED:
        token = generate_email_verification_token(email=user.email)
        send_new_account_email(email_to=user.email, username=user.name, token=token)

    return Message(
        message="Registration successful. Please check your @troy.edu email to verify your account."
    )


@router.get("/verify-email", response_model=Message)
def verify_email(session: SessionDep, token: str) -> Message:
    """
    Verify a user's email address with a token from the verification email.
    """
    email = verify_email_verification_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired verification token.")

    user = crud.get_user_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this email does not exist in the system.",
        )
    if user.is_verified:
        raise HTTPException(
            status_code=400, detail="This email address has already been verified."
        )

    # Update user status and assign default permissions
    user.is_verified = True
    user.permissions = ["document:read"]
    session.add(user)
    session.commit()

    return Message(message="Email verified successfully. You can now log in.")

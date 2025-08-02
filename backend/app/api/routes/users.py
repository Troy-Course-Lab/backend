from fastapi import APIRouter, HTTPException

from app import crud
from app.api.deps import SessionDep
from app.schemas import Message, User, UserCreate

router = APIRouter()


@router.post("/register", response_model=Message, status_code=201)
def register_new_user(session: SessionDep, user_in: UserCreate) -> Message:
    """
    Create new user.
    - Validates that the email is a @troy.edu address.
    - Sets the user as unverified by default.
    """
    # Validate email domain
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

    # Create the user with is_verified=False
    # The role defaults to 'user' as defined in the model.
    crud.create_user(session=session, user_in=user_in)

    # In a real application, you would trigger an email verification flow here.
    # For example:
    # verification_code = generate_verification_code()
    # store_verification_code(user_in.email, verification_code)
    # send_verification_email(email_to=user_in.email, code=verification_code)

    return Message(
        message="Registration successful. Please check your @troy.edu email for a verification code."
    )

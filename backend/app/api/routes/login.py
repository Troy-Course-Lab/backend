from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app import crud
from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.schemas import Token

router = APIRouter()


@router.post("/login/access-token", response_model=Token)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = crud.authenticate(
        session=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    # Add a check to ensure the user has verified their email
    if not user.is_verified:
        raise HTTPException(
            status_code=401,
            detail="Account not verified. Please check your email.",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Add role and permissions to the JWT payload
    additional_claims = {"role": user.role, "permissions": user.permissions}
    
    access_token = security.create_access_token(
        user.email,
        expires_delta=access_token_expires,
        additional_claims=additional_claims,
    )

    return Token(access_token=access_token)

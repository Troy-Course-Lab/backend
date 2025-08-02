from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlmodel import Session

from app import crud
from app.core import security
from app.core.config import settings
from app.core.db import engine
from app.models import User
from app.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # The 'sub' field in the token is expected to be the user's email.
    user = crud.get_user_by_email(session=session, email=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_verified_user(current_user: CurrentUser) -> User:
    """
    Dependency to get the current user, ensuring they are active and verified.
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    if not current_user.is_verified:
        raise HTTPException(status_code=400, detail="User has not verified email.")
    return current_user


def require_permission(required_permissions: list[str]):
    """
    Dependency factory to check if the current user has the required permissions.
    - Admin Level 2 ('admin2') bypasses all permission checks.
    - Checks if the user's permissions are a superset of the required permissions.
    """

    def permission_checker(
        current_user: User = Depends(get_current_active_verified_user),
    ):
        if "admin2" == current_user.role:
            return current_user

        user_permissions = set(current_user.permissions)
        if not set(required_permissions).issubset(user_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have sufficient permissions.",
            )
        return current_user

    return permission_checker

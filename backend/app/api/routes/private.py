import uuid
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import func, select

# Corrected dependency import to use the new role-based checker
from app.api.deps import get_current_admin2_user, SessionDep
# Corrected schema import path
from app.schemas import User
from app.models import User as UserModel

router = APIRouter(
    prefix="/private",
    tags=["private"],
    # Updated dependency to protect all routes in this file
    dependencies=[Depends(get_current_admin2_user)],
)


@router.get("/users-count/", response_model=int)
def read_users_count(session: SessionDep) -> Any:
    """
    Retrieve the total number of users in the system.
    (Requires admin2 privileges)
    """
    count_statement = select(func.count()).select_from(UserModel)
    count = session.exec(count_statement).one()
    return count


@router.get("/user/{user_id}", response_model=User)
def read_user_by_id(user_id: uuid.UUID, session: SessionDep) -> Any:
    """
    Get a specific user by their UUID.
    (Requires admin2 privileges)
    """
    user = session.get(UserModel, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

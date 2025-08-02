import uuid
from typing import List

from sqlalchemy import ARRAY, Column, String
from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    id_troy: str = Field(unique=True, index=True, nullable=False)
    name: str = Field(index=True, nullable=False)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    major: str | None = Field(default=None)
    class_: str | None = Field(default=None, alias="class")

    # Role definition: 'user', 'admin1', 'admin2'
    role: str = Field(default="user", nullable=False)

    # Granular permissions
    permissions: List[str] = Field(
        sa_column=Column(ARRAY(String), nullable=False, server_default="{}"),
        default_factory=list,
    )

    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)

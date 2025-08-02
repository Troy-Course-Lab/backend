import uuid
from typing import List

from pydantic import BaseModel, EmailStr


# Properties to receive via API on user creation
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    major: str | None = None
    class_: str | None = None
    role: str = "user"


# Properties to receive via API on user update
class UserUpdate(BaseModel):
    password: str | None = None
    name: str | None = None
    major: str | None = None
    class_: str | None = None


# Base properties stored in DB
class UserInDBBase(BaseModel):
    id: uuid.UUID
    id_troy: str
    name: str
    email: EmailStr
    major: str | None = None
    class_: str | None = None
    role: str
    permissions: List[str]
    is_active: bool
    is_verified: bool

    class Config:
        from_attributes = True


# Properties to return to client
class User(UserInDBBase):
    pass


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str | None = None


class Message(BaseModel):
    message: str

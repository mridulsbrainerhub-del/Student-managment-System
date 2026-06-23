from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )
    age: int
    roll_number: str
    class_id: int | None = None
    address: str | None = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )
    age: int | None = None
    roll_number: str | None = None
    class_id: int | None = None
    address: str | None = None


class StudentResponse(StudentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
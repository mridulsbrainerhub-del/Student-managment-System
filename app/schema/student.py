from datetime import datetime
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class StudentBase(BaseModel):
    full_name: str
    age: int
    gender: Literal["male", "female", "other"]

    father_name: str
    dob: str

    class_name: int
    section: str = Field(min_length=1, max_length=1)

    mobile_number: str = Field(min_length=10, max_length=10, pattern=r"^\d+$")
    email: EmailStr

    roll_number: int
    address: str | None = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: str | None = None
    age: int | None = None
    gender: Literal["male", "female", "other"] | None = None

    father_name: str | None = None
    dob: str | None = None

    class_name: int | None = None
    section: str | None = Field(default=None, min_length=1, max_length=1)

    mobile_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )
    email: EmailStr | None = None

    roll_number: int | None = None
    address: str | None = None


class StudentResponse(BaseModel):
    id: UUID

    full_name: str
    age: int
    gender: str

    father_name: str
    dob: str

    class_name: int
    section: str

    mobile_number: str
    email: EmailStr

    roll_number: int
    address: str | None = None

    created_at: datetime
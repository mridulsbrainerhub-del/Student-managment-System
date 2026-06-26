from datetime import datetime
from uuid import UUID
from typing import Literal

from pydantic import BaseModel, EmailStr, Field


class TeacherBase(BaseModel):
    teacher_code: str

    name: str
    age: int
    gender: Literal["male", "female", "other"]

    father_name: str
    dob: str

    mobile_number: str = Field(
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )

    email: EmailStr
    department: str | None = None

    subject_names: list[str] = []


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    teacher_code: str | None = None

    name: str | None = None
    age: int | None = None
    gender: Literal["male", "female", "other"] | None = None

    father_name: str | None = None
    dob: str | None = None

    mobile_number: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )

    email: EmailStr | None = None
    department: str | None = None

    subject_names: list[str] | None = None


class TeacherResponse(BaseModel):
    id: UUID
    teacher_code: str

    name: str
    age: int
    gender: str

    father_name: str
    dob: str

    mobile_number: str
    email: EmailStr
    department: str | None = None

    subject_names: list[str]

    created_at: datetime
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SchoolClassBase(BaseModel):
    name: int
    section: str = Field(min_length=1, max_length=1)
    room_number: str | None = None
    batch_year: int
    incharge_teacher_code: str | None = None


class SchoolClassCreate(SchoolClassBase):
    pass


class SchoolClassUpdate(BaseModel):
    name: int | None = None
    section: str | None = Field(default=None, min_length=1, max_length=1)
    room_number: str | None = None
    batch_year: int | None = None
    incharge_teacher_code: str | None = None


class SchoolClassResponse(BaseModel):
    id: UUID

    name: int
    section: str
    room_number: str | None = None
    batch_year: int

    incharge_teacher_name: str | None = None
    incharge_teacher_code: str | None = None
    incharge_teacher_phone: str | None = None

    total_students: int
    subjects: list[str]

    created_at: datetime
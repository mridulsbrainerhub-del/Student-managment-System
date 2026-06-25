from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SchoolClassBase(BaseModel):
    name: str
    section: str
    room_number: str | None = None
    batch_year: str
    incharge_teacher_id: UUID | None = None


class SchoolClassCreate(SchoolClassBase):
    pass


class SchoolClassUpdate(BaseModel):
    name: str | None = None
    section: str | None = None
    room_number: str | None = None
    batch_year: str | None = None
    incharge_teacher_id: UUID | None = None


class SchoolClassResponse(SchoolClassBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
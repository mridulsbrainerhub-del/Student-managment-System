from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class GradeCreate(BaseModel):
    student_id: UUID
    subject: str
    marks: int
    total_marks: int = 100


class GradeUpdate(BaseModel):
    subject: str | None = None
    marks: int | None = None
    total_marks: int | None = None


class GradeResponse(BaseModel):
    id: UUID
    student_id: UUID
    subject: str
    marks: int
    total_marks: int
    created_at: datetime

    class Config:
        from_attributes = True
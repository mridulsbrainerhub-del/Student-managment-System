from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class GradeCreate(BaseModel):
    student_roll_number: int
    class_name: int
    section: str = Field(min_length=1, max_length=1)

    subject_name: str

    marks: int = Field(ge=0)
    total_marks: int = Field(gt=0)

    @model_validator(mode="after")
    def validate_marks(self):
        if self.marks > self.total_marks:
            raise ValueError("marks cannot be greater than total_marks")
        return self


class GradeUpdate(BaseModel):
    subject_name: str | None = None
    marks: int | None = Field(default=None, ge=0)
    total_marks: int | None = Field(default=None, gt=0)


class GradeResponse(BaseModel):
    id: UUID

    student_name: str
    student_roll_number: int

    class_name: int
    section: str

    subject_name: str

    marks: int
    total_marks: int
    percentage: float

    created_at: datetime

    class Config:
        from_attributes = True
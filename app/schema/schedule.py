from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class ScheduleBase(BaseModel):
    class_name: int
    section: str = Field(min_length=1, max_length=1)

    teacher_code: str
    subject_name: str

    day: str
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("end_time must be after start_time")
        return self


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    class_name: int | None = None
    section: str | None = Field(default=None, min_length=1, max_length=1)

    teacher_code: str | None = None
    subject_name: str | None = None

    day: str | None = None
    start_time: time | None = None
    end_time: time | None = None


class ScheduleResponse(BaseModel):
    id: UUID

    class_name: int
    section: str

    teacher_name: str
    teacher_code: str

    subject_name: str

    day: str
    start_time: time
    end_time: time

    created_at: datetime
from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel


class ScheduleBase(BaseModel):
    class_id: UUID
    teacher_id: UUID
    subject: str
    day: str
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    class_id: UUID | None = None
    teacher_id: UUID | None = None
    subject: str | None = None
    day: str | None = None
    start_time: time | None = None
    end_time: time | None = None


class ScheduleResponse(ScheduleBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
from datetime import datetime, time
from pydantic import BaseModel
from uuid import UUID

class ScheduleBase(BaseModel):
    class_id: int
    teacher_id: int
    subject: str
    day: str
    start_time: time
    end_time: time


class ScheduleCreate(ScheduleBase):
    pass


class ScheduleUpdate(BaseModel):
    class_id: int | None = None
    teacher_id: int | None = None
    subject: str | None = None
    day: str | None = None
    start_time: time | None = None
    end_time: time | None = None


class ScheduleResponse(ScheduleBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True
from datetime import datetime
from pydantic import BaseModel


class SchoolClassBase(BaseModel):
    name: str
    section: str
    room_number: str | None = None


class SchoolClassCreate(SchoolClassBase):
    pass


class SchoolClassUpdate(BaseModel):
    name: str | None = None
    section: str | None = None
    room_number: str | None = None


class SchoolClassResponse(SchoolClassBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
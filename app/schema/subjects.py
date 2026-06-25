from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class SubjectCreate(BaseModel):
    name: str
    class_name: str
    is_optional: bool = False


class SubjectUpdate(BaseModel):
    name: str | None = None
    is_optional: bool | None = None


class SubjectResponse(BaseModel):
    id: UUID
    name: str
    class_id: UUID
    is_optional: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
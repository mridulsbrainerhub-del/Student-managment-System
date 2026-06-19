from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


class TeacherBase(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )
    subject: str
    department: str | None = None


class TeacherCreate(TeacherBase):
    pass


class TeacherUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    phone: str | None = Field(
        default=None,
        min_length=10,
        max_length=10,
        pattern=r"^\d+$"
    )
    subject: str | None = None
    department: str | None = None


class TeacherResponse(TeacherBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
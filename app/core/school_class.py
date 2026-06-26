import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    __table_args__ = (
        UniqueConstraint(
            "name",
            "section",
            "batch_year",
            name="uq_class_section_batch"
        ),
    )

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    name = Column(Integer, nullable=False)  # 10, 11, 12
    section = Column(String(1), nullable=False)  # A, B, C
    room_number = Column(String, nullable=True)
    batch_year = Column(Integer, nullable=False)

    incharge_teacher_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teachers.id"),
        nullable=True
    )

    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship(
        "Student",
        back_populates="school_class",
        cascade="all, delete-orphan"
    )

    subjects = relationship(
        "Subject",
        back_populates="school_class",
        cascade="all, delete-orphan"
    )

    schedules = relationship(
        "Schedule",
        back_populates="school_class",
        cascade="all, delete-orphan"
    )

    incharge_teacher = relationship(
        "Teacher",
        back_populates="incharge_classes"
    )
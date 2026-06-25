import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Table
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


# Many-to-many table: teachers <-> subjects
teacher_subjects = Table(
    "teacher_subjects",
    Base.metadata,

    Column(
        "teacher_id",
        UUID(as_uuid=True),
        ForeignKey("teachers.id", ondelete="CASCADE"),
        primary_key=True
    ),

    Column(
        "subject_id",
        UUID(as_uuid=True),
        ForeignKey("subjects.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    name = Column(String, nullable=False)

    class_id = Column(
        UUID(as_uuid=True),
        ForeignKey("classes.id", ondelete="CASCADE"),
        nullable=False
    )

    is_optional = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Subject belongs to one class
    school_class = relationship(
        "SchoolClass",
        back_populates="subjects"
    )

    # One subject can have many teachers
    # One teacher can have many subjects
    teachers = relationship(
        "Teacher",
        secondary=teacher_subjects,
        back_populates="subjects"
    )

    # Subject can have overview/details
    overview = relationship(
        "SubjectOverview",
        back_populates="subject",
        cascade="all, delete-orphan"
    )
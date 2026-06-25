import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base
from app.core.subjects import teacher_subjects


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    teacher_code = Column(String, unique=True, index=True, nullable=False)

    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    gender = Column(String, nullable=False)
    father_name = Column(String, nullable=False)
    dob = Column(String, nullable=False)

    mobile_number = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    department = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    subjects = relationship(
        "Subject",
        secondary=teacher_subjects,
        back_populates="teachers"
    )

    incharge_classes = relationship(
        "SchoolClass",
        back_populates="incharge_teacher"
    )
import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class Student(Base):
    __tablename__ = "students"

    __table_args__ = (
        UniqueConstraint("class_id", "roll_number", name="uq_student_class_roll_number"),
    )

    
    full_name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    gender = Column(String, nullable=False)

    father_name = Column(String, nullable=False)
    dob = Column(String, nullable=False)

    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)

    mobile_number = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)

    roll_number = Column(Integer, nullable=False)

    address = Column(String, nullable=True)
    description = Column(String, nullable=True)
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    school_class = relationship("SchoolClass", back_populates="students")
    grades = relationship(
        "Grade",
        back_populates="student",
        cascade="all, delete-orphan"
    )
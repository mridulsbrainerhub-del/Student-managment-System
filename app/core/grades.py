import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class Grade(Base):
    __tablename__ = "grades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)

    marks = Column(Integer, nullable=False)
    total_marks = Column(Integer, nullable=False)
    

    created_at = Column(DateTime, default=datetime.utcnow)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")
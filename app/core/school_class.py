from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.database.database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    section = Column(String, nullable=False)
    room_number = Column(String, nullable=True)
    batch_year = Column(String, nullable=False)

    incharge_teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship("Student", back_populates="school_class")
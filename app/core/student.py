import uuid
from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    age = Column(Integer, nullable=False)
    roll_number = Column(String, unique=True, index=True, nullable=False)

    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=True)

    description = Column(String, nullable=True)


    address = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    school_class = relationship("SchoolClass", back_populates="students")
    grades = relationship("Grade", back_populates="student")
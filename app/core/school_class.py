import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    name = Column(String, nullable=False)
    section = Column(String, nullable=False)
    room_number = Column(String, nullable=True)
    batch_year = Column(String, nullable=False)

    incharge_teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    students = relationship("Student", back_populates="school_class")
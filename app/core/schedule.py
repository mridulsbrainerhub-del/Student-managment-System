import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, ForeignKey, Time
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    class_id = Column(UUID(as_uuid=True), ForeignKey("classes.id"), nullable=False)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(UUID(as_uuid=True), ForeignKey("teachers.id"), nullable=False)

    day = Column(String, nullable=False)

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
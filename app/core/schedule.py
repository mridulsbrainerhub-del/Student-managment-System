from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Time
from datetime import datetime

from app.database.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)

    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"), nullable=False)

    subject = Column(String, nullable=False)

    day = Column(String, nullable=False)  # Monday, Tuesday, etc.

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)
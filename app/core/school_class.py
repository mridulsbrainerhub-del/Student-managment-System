from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    section = Column(String, nullable=False)
    room_number = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
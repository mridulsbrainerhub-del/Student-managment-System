# student model is here 
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base

# student table is here 
class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=True)

    age = Column(Integer, nullable=False)
    roll_number = Column(String, unique=True, index=True, nullable=False)
    class_name = Column(String, nullable=False)
    address = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)




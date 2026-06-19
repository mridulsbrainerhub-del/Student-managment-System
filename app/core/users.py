from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database.database import Base

# user table is here 
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="student")

    created_at = Column(DateTime, default=datetime.utcnow)
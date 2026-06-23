import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base


# user table is here
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    role = Column(String, default="student")

    created_at = Column(DateTime, default=datetime.utcnow)
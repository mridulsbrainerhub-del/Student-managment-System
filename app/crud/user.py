from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.users import User
from app.schema.users import UserCreate
from app.core.auth import hash_password


def handle_user_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "email" in message:
        detail = "Email already registered"
    elif "unique constraint" in message:
        detail = "Duplicate user data"
    else:
        detail = "Invalid user data"

    raise HTTPException(
        status_code=400,
        detail=detail
    )


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = hash_password(user.password)

    db_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    db.add(db_user)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as error:
        db.rollback()
        handle_user_integrity_error(error)
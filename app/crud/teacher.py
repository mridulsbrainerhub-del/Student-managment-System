from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.teacher import Teacher
from app.schema.teacher import TeacherCreate, TeacherUpdate


def handle_teacher_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "email" in message:
        detail = "Email already exists"
    elif "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Related record does not exist"
    else:
        detail = "Invalid teacher data"

    raise HTTPException(
        status_code=400,
        detail=detail
    )


def create_teacher(db: Session, teacher: TeacherCreate):
    db_teacher = Teacher(
        name=teacher.name,
        email=teacher.email,
        phone=teacher.phone,
        subject=teacher.subject,
        department=teacher.department
    )

    db.add(db_teacher)

    try:
        db.commit()
        db.refresh(db_teacher)
        return db_teacher
    except IntegrityError as error:
        db.rollback()
        handle_teacher_integrity_error(error)


def get_teachers(db: Session):
    return db.query(Teacher).all()


def get_teacher_by_id(db: Session, teacher_id: UUID):
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()


def get_teacher_by_email(db: Session, email: str):
    return db.query(Teacher).filter(Teacher.email == email).first()


def update_teacher_full(
    db: Session,
    teacher_id: UUID,
    teacher_data: TeacherCreate
):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        return None

    teacher.name = teacher_data.name
    teacher.email = teacher_data.email
    teacher.phone = teacher_data.phone
    teacher.subject = teacher_data.subject
    teacher.department = teacher_data.department

    try:
        db.commit()
        db.refresh(teacher)
        return teacher
    except IntegrityError as error:
        db.rollback()
        handle_teacher_integrity_error(error)


def update_teacher_partial(
    db: Session,
    teacher_id: UUID,
    teacher_data: TeacherUpdate
):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        return None

    update_data = teacher_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(teacher, key, value)

    try:
        db.commit()
        db.refresh(teacher)
        return teacher
    except IntegrityError as error:
        db.rollback()
        handle_teacher_integrity_error(error)


def delete_teacher(db: Session, teacher_id: UUID):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        return None

    db.delete(teacher)
    db.commit()

    return teacher
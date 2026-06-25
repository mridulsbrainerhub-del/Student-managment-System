from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.subjects import Subject
from app.core.school_class import SchoolClass
from app.schema.subjects import SubjectCreate, SubjectUpdate


def handle_subject_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Class does not exist"
    elif "unique constraint" in message:
        detail = "Subject already exists for this class"
    else:
        detail = "Invalid subject data"

    raise HTTPException(
        status_code=400,
        detail=detail
    )


def create_subject(db: Session, subject: SubjectCreate):
    school_class = (
        db.query(SchoolClass)
        .filter(SchoolClass.name == subject.class_name)
        .first()
    )

    if school_class is None:
        return None

    db_subject = Subject(
        name=subject.name,
        class_id=school_class.id,
        is_optional=subject.is_optional
    )

    db.add(db_subject)

    try:
        db.commit()
        db.refresh(db_subject)
        return db_subject
    except IntegrityError as error:
        db.rollback()
        handle_subject_integrity_error(error)


def get_subjects(db: Session):
    return db.query(Subject).all()


def get_subjects_by_class_name(db: Session, class_name: str):
    school_class = (
        db.query(SchoolClass)
        .filter(SchoolClass.name == class_name)
        .first()
    )

    if school_class is None:
        return None

    return db.query(Subject).filter(Subject.class_id == school_class.id).all()


def get_subject_by_class_and_name(
    db: Session,
    class_name: str,
    subject_name: str
):
    school_class = (
        db.query(SchoolClass)
        .filter(SchoolClass.name == class_name)
        .first()
    )

    if school_class is None:
        return None

    return (
        db.query(Subject)
        .filter(
            Subject.class_id == school_class.id,
            Subject.name == subject_name
        )
        .first()
    )


def update_subject_by_class_and_name(
    db: Session,
    class_name: str,
    subject_name: str,
    subject_update: SubjectUpdate
):
    subject = get_subject_by_class_and_name(db, class_name, subject_name)

    if subject is None:
        return None

    update_data = subject_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(subject, key, value)

    try:
        db.commit()
        db.refresh(subject)
        return subject
    except IntegrityError as error:
        db.rollback()
        handle_subject_integrity_error(error)


def delete_subject_by_class_and_name(
    db: Session,
    class_name: str,
    subject_name: str
):
    subject = get_subject_by_class_and_name(db, class_name, subject_name)

    if subject is None:
        return None

    db.delete(subject)
    db.commit()

    return subject
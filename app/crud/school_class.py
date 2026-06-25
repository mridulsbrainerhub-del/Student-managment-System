from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.school_class import SchoolClass
from app.schema.school_class import SchoolClassCreate, SchoolClassUpdate


def handle_school_class_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Incharge teacher does not exist"
    elif "unique constraint" in message:
        detail = "Class and section already exists"
    else:
        detail = "Invalid class data"

    raise HTTPException(
        status_code=400,
        detail=detail
    )


def create_school_class(db: Session, school_class: SchoolClassCreate):
    db_school_class = SchoolClass(
        name=school_class.name,
        section=school_class.section,
        room_number=school_class.room_number,
        batch_year=school_class.batch_year,
        incharge_teacher_id=school_class.incharge_teacher_id
    )

    db.add(db_school_class)

    try:
        db.commit()
        db.refresh(db_school_class)
        return db_school_class
    except IntegrityError as error:
        db.rollback()
        handle_school_class_integrity_error(error)


def get_school_classes(db: Session):
    return db.query(SchoolClass).all()


def get_school_class_by_id(db: Session, class_id: UUID):
    return db.query(SchoolClass).filter(SchoolClass.id == class_id).first()


def get_school_class_by_name_section(db: Session, name: str, section: str):
    return (
        db.query(SchoolClass)
        .filter(SchoolClass.name == name, SchoolClass.section == section)
        .first()
    )


def update_school_class_full(
    db: Session,
    class_id: UUID,
    class_data: SchoolClassCreate
):
    school_class = get_school_class_by_id(db, class_id)

    if school_class is None:
        return None

    school_class.name = class_data.name
    school_class.section = class_data.section
    school_class.room_number = class_data.room_number
    school_class.batch_year = class_data.batch_year
    school_class.incharge_teacher_id = class_data.incharge_teacher_id

    try:
        db.commit()
        db.refresh(school_class)
        return school_class
    except IntegrityError as error:
        db.rollback()
        handle_school_class_integrity_error(error)


def update_school_class_partial(
    db: Session,
    class_id: UUID,
    class_data: SchoolClassUpdate
):
    school_class = get_school_class_by_id(db, class_id)

    if school_class is None:
        return None

    update_data = class_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(school_class, key, value)

    try:
        db.commit()
        db.refresh(school_class)
        return school_class
    except IntegrityError as error:
        db.rollback()
        handle_school_class_integrity_error(error)


def delete_school_class(db: Session, class_id: UUID):
    school_class = get_school_class_by_id(db, class_id)

    if school_class is None:
        return None

    db.delete(school_class)
    db.commit()

    return school_class
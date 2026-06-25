from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.school_class import SchoolClass
from app.core.teacher import Teacher
from app.schema.school_class import SchoolClassCreate, SchoolClassUpdate


def handle_school_class_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Incharge teacher does not exist"
    elif "unique" in message or "uq_class_section_batch" in message:
        detail = "Class, section, and batch year already exists"
    else:
        detail = "Invalid class data"

    raise HTTPException(status_code=400, detail=detail)


def get_teacher_by_code(db: Session, teacher_code: str | None):
    if teacher_code is None:
        return None

    teacher = db.query(Teacher).filter(
        Teacher.teacher_code == teacher_code
    ).first()

    if teacher is None:
        raise HTTPException(
            status_code=404,
            detail="Incharge teacher not found"
        )

    return teacher


def create_school_class(db: Session, school_class: SchoolClassCreate):
    incharge_teacher = get_teacher_by_code(
        db,
        school_class.incharge_teacher_code
    )

    db_school_class = SchoolClass(
        name=school_class.name,
        section=school_class.section,
        room_number=school_class.room_number,
        batch_year=school_class.batch_year,
        incharge_teacher_id=incharge_teacher.id if incharge_teacher else None
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


def get_school_class_by_name_section(
    db: Session,
    name: int,
    section: str
):
    return db.query(SchoolClass).filter(
        SchoolClass.name == name,
        SchoolClass.section == section
    ).first()


def update_school_class_full(
    db: Session,
    name: int,
    section: str,
    class_data: SchoolClassCreate
):
    school_class = get_school_class_by_name_section(
        db,
        name,
        section
    )

    if school_class is None:
        return None

    incharge_teacher = get_teacher_by_code(
        db,
        class_data.incharge_teacher_code
    )

    school_class.name = class_data.name
    school_class.section = class_data.section
    school_class.room_number = class_data.room_number
    school_class.batch_year = class_data.batch_year
    school_class.incharge_teacher_id = incharge_teacher.id if incharge_teacher else None

    try:
        db.commit()
        db.refresh(school_class)
        return school_class
    except IntegrityError as error:
        db.rollback()
        handle_school_class_integrity_error(error)


def update_school_class_partial(
    db: Session,
    name: int,
    section: str,
    class_data: SchoolClassUpdate
):
    school_class = get_school_class_by_name_section(
        db,
        name,
        section
    )

    if school_class is None:
        return None

    update_data = class_data.model_dump(exclude_unset=True)

    if "incharge_teacher_code" in update_data:
        teacher_code = update_data.pop("incharge_teacher_code")
        incharge_teacher = get_teacher_by_code(db, teacher_code)
        school_class.incharge_teacher_id = (
            incharge_teacher.id if incharge_teacher else None
        )

    for key, value in update_data.items():
        setattr(school_class, key, value)

    try:
        db.commit()
        db.refresh(school_class)
        return school_class
    except IntegrityError as error:
        db.rollback()
        handle_school_class_integrity_error(error)


def delete_school_class(
    db: Session,
    name: int,
    section: str
):
    school_class = get_school_class_by_name_section(
        db,
        name,
        section
    )

    if school_class is None:
        return None

    db.delete(school_class)
    db.commit()

    return school_class
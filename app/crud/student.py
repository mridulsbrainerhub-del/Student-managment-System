from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.student import Student
from app.core.school_class import SchoolClass
from app.schema.student import StudentCreate, StudentUpdate


def handle_student_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "email" in message:
        detail = "Email already exists"
    elif "roll_number" in message:
        detail = "Roll number already exists"
    elif "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Class does not exist"
    else:
        detail = "Invalid student data"

    raise HTTPException(status_code=400, detail=detail)


def get_class_id_by_name(db: Session, class_name: str | None):
    if class_name is None:
        return None

    school_class = db.query(SchoolClass).filter(
        SchoolClass.name == class_name
    ).first()

    if school_class is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    return school_class.id


def create_student(db: Session, student: StudentCreate):
    class_id = get_class_id_by_name(db, student.class_name)

    db_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        age=student.age,
        roll_number=student.roll_number,
        class_id=class_id,
        address=student.address
    )

    db.add(db_student)

    try:
        db.commit()
        db.refresh(db_student)
        return db_student
    except IntegrityError as error:
        db.rollback()
        handle_student_integrity_error(error)


def get_students(db: Session):
    return db.query(Student).all()


def get_student_by_id(db: Session, student_id: UUID):
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()


def get_student_by_roll_number(db: Session, roll_number: str):
    return db.query(Student).filter(Student.roll_number == roll_number).first()


def update_student_full(
    db: Session,
    roll_number: str,
    student_data: StudentCreate
):
    student = get_student_by_roll_number(db, roll_number)

    if student is None:
        return None

    class_id = get_class_id_by_name(db, student_data.class_name)

    student.name = student_data.name
    student.email = student_data.email
    student.phone = student_data.phone
    student.age = student_data.age
    student.roll_number = student_data.roll_number
    student.class_id = class_id
    student.address = student_data.address

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as error:
        db.rollback()
        handle_student_integrity_error(error)


def update_student_partial(
    db: Session,
    roll_number: str,
    student_data: StudentUpdate
):
    student = get_student_by_roll_number(db, roll_number)

    if student is None:
        return None

    update_data = student_data.model_dump(exclude_unset=True)

    if "class_name" in update_data:
        class_name = update_data.pop("class_name")
        student.class_id = get_class_id_by_name(db, class_name)

    for key, value in update_data.items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as error:
        db.rollback()
        handle_student_integrity_error(error)


def delete_student(db: Session, roll_number: str):
    student = get_student_by_roll_number(db, roll_number)

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student
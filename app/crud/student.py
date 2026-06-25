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
    elif "roll_number" in message or "uq_student_class_roll_number" in message:
        detail = "Roll number already exists in this class"
    elif "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Class does not exist"
    else:
        detail = "Invalid student data"

    raise HTTPException(status_code=400, detail=detail)


def get_class_by_name_and_section(db: Session, class_name: int, section: str):
    school_class = db.query(SchoolClass).filter(
        SchoolClass.name == class_name,
        SchoolClass.section == section
    ).first()

    if school_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return school_class


def create_student(db: Session, student: StudentCreate):
    school_class = get_class_by_name_and_section(
        db,
        student.class_name,
        student.section
    )

    db_student = Student(
        full_name=student.full_name,
        age=student.age,
        gender=student.gender,
        father_name=student.father_name,
        dob=student.dob,
        class_id=school_class.id,
        mobile_number=student.mobile_number,
        email=student.email,
        roll_number=student.roll_number,
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


def get_student_by_roll_class_section(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str
):
    school_class = get_class_by_name_and_section(db, class_name, section)

    return db.query(Student).filter(
        Student.roll_number == roll_number,
        Student.class_id == school_class.id
    ).first()


def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()


def update_student_full(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str,
    student_data: StudentCreate
):
    student = get_student_by_roll_class_section(
        db,
        roll_number,
        class_name,
        section
    )

    if student is None:
        return None

    new_class = get_class_by_name_and_section(
        db,
        student_data.class_name,
        student_data.section
    )

    student.full_name = student_data.full_name
    student.age = student_data.age
    student.gender = student_data.gender
    student.father_name = student_data.father_name
    student.dob = student_data.dob
    student.class_id = new_class.id
    student.mobile_number = student_data.mobile_number
    student.email = student_data.email
    student.roll_number = student_data.roll_number
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
    roll_number: int,
    class_name: int,
    section: str,
    student_data: StudentUpdate
):
    student = get_student_by_roll_class_section(
        db,
        roll_number,
        class_name,
        section
    )

    if student is None:
        return None

    update_data = student_data.model_dump(exclude_unset=True)

    if "class_name" in update_data or "section" in update_data:
        new_class_name = update_data.pop("class_name", class_name)
        new_section = update_data.pop("section", section)

        new_class = get_class_by_name_and_section(
            db,
            new_class_name,
            new_section
        )

        student.class_id = new_class.id

    for key, value in update_data.items():
        setattr(student, key, value)

    try:
        db.commit()
        db.refresh(student)
        return student
    except IntegrityError as error:
        db.rollback()
        handle_student_integrity_error(error)


def delete_student(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str
):
    student = get_student_by_roll_class_section(
        db,
        roll_number,
        class_name,
        section
    )

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student
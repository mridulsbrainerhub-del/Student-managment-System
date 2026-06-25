from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.grades import Grade
from app.core.student import Student
from app.core.school_class import SchoolClass
from app.core.subjects import Subject
from app.schema.grades import GradeCreate, GradeUpdate


def handle_grade_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Related record does not exist"
    else:
        detail = "Invalid grade data"

    raise HTTPException(status_code=400, detail=detail)


def get_class_by_name_and_section(db: Session, class_name: int, section: str):
    school_class = db.query(SchoolClass).filter(
        SchoolClass.name == class_name,
        SchoolClass.section == section
    ).first()

    if school_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return school_class


def get_student_by_roll_class_section(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str
):
    school_class = get_class_by_name_and_section(db, class_name, section)

    student = db.query(Student).filter(
        Student.roll_number == roll_number,
        Student.class_id == school_class.id
    ).first()

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


def get_subject_by_name_and_class(
    db: Session,
    subject_name: str,
    class_name: int,
    section: str
):
    school_class = get_class_by_name_and_section(db, class_name, section)

    subject = db.query(Subject).filter(
        Subject.name == subject_name,
        Subject.class_id == school_class.id
    ).first()

    if subject is None:
        raise HTTPException(status_code=404, detail="Subject not found in this class")

    return subject


def get_grade_by_student_and_subject(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str,
    subject_name: str
):
    student = get_student_by_roll_class_section(
        db,
        roll_number,
        class_name,
        section
    )

    subject = get_subject_by_name_and_class(
        db,
        subject_name,
        class_name,
        section
    )

    return db.query(Grade).filter(
        Grade.student_id == student.id,
        Grade.subject_id == subject.id
    ).first()


def create_grade(db: Session, grade: GradeCreate):
    student = get_student_by_roll_class_section(
        db,
        grade.student_roll_number,
        grade.class_name,
        grade.section
    )

    subject = get_subject_by_name_and_class(
        db,
        grade.subject_name,
        grade.class_name,
        grade.section
    )

    db_grade = Grade(
        student_id=student.id,
        subject_id=subject.id,
        marks=grade.marks,
        total_marks=grade.total_marks
    )

    db.add(db_grade)

    try:
        db.commit()
        db.refresh(db_grade)
        return db_grade
    except IntegrityError as error:
        db.rollback()
        handle_grade_integrity_error(error)


def get_grades_by_student(
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

    return db.query(Grade).filter(
        Grade.student_id == student.id
    ).all()


def update_grade(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str,
    subject_name: str,
    grade_data: GradeUpdate
):
    grade = get_grade_by_student_and_subject(
        db,
        roll_number,
        class_name,
        section,
        subject_name
    )

    if grade is None:
        return None

    update_data = grade_data.model_dump(exclude_unset=True)

    if "subject_name" in update_data:
        new_subject_name = update_data.pop("subject_name")

        new_subject = get_subject_by_name_and_class(
            db,
            new_subject_name,
            class_name,
            section
        )

        grade.subject_id = new_subject.id

    for key, value in update_data.items():
        setattr(grade, key, value)

    try:
        db.commit()
        db.refresh(grade)
        return grade
    except IntegrityError as error:
        db.rollback()
        handle_grade_integrity_error(error)


def delete_grade(
    db: Session,
    roll_number: int,
    class_name: int,
    section: str,
    subject_name: str
):
    grade = get_grade_by_student_and_subject(
        db,
        roll_number,
        class_name,
        section,
        subject_name
    )

    if grade is None:
        return None

    db.delete(grade)
    db.commit()

    return grade
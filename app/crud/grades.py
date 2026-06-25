from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.grades import Grade
from app.core.student import Student
from app.schema.grades import GradeCreate, GradeUpdate


def handle_grade_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Student does not exist"
    else:
        detail = "Invalid grade data"

    raise HTTPException(
        status_code=400,
        detail=detail
    )


def create_grade(db: Session, grade: GradeCreate):
    db_grade = Grade(
        student_id=grade.student_id,
        subject=grade.subject,
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


def get_grade_by_id(db: Session, grade_id: UUID):
    return db.query(Grade).filter(Grade.id == grade_id).first()


def get_grades_by_student_email(db: Session, email: str):
    student = db.query(Student).filter(Student.email == email).first()

    if student is None:
        return None

    grades = db.query(Grade).filter(Grade.student_id == student.id).all()

    return {
        "student": student,
        "grades": grades
    }


def update_grade(db: Session, grade_id: UUID, grade_data: GradeUpdate):
    grade = get_grade_by_id(db, grade_id)

    if grade is None:
        return None

    update_data = grade_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(grade, key, value)

    try:
        db.commit()
        db.refresh(grade)
        return grade
    except IntegrityError as error:
        db.rollback()
        handle_grade_integrity_error(error)


def delete_grade(db: Session, grade_id: UUID):
    grade = get_grade_by_id(db, grade_id)

    if grade is None:
        return None

    db.delete(grade)
    db.commit()

    return grade
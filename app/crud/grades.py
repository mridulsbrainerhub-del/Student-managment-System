from uuid import UUID

from sqlalchemy.orm import Session

from app.core.grades import Grade
from app.core.student import Student
from app.schema.grades import GradeCreate, GradeUpdate


def create_grade(db: Session, grade: GradeCreate):
    db_grade = Grade(
        student_id=grade.student_id,
        subject=grade.subject,
        marks=grade.marks,
        total_marks=grade.total_marks
    )

    db.add(db_grade)
    db.commit()
    db.refresh(db_grade)

    return db_grade


def get_grades(db: Session):
    return db.query(Grade).all()


def get_grade_by_id(db: Session, grade_id: UUID):
    return db.query(Grade).filter(Grade.id == grade_id).first()


def get_grades_by_student_id(db: Session, student_id: UUID):
    return db.query(Grade).filter(Grade.student_id == student_id).all()


def get_grades_by_student_email(db: Session, email: str):
    student = db.query(Student).filter(Student.email == email).first()

    if student is None:
        return None

    return {
        "student": student,
        "grades": student.grades
    }


def update_grade(
    db: Session,
    grade_id: UUID,
    grade_data: GradeUpdate
):
    grade = get_grade_by_id(db, grade_id)

    if grade is None:
        return None

    update_data = grade_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(grade, key, value)

    db.commit()
    db.refresh(grade)

    return grade


def delete_grade(db: Session, grade_id: UUID):
    grade = get_grade_by_id(db, grade_id)

    if grade is None:
        return None

    db.delete(grade)
    db.commit()

    return grade
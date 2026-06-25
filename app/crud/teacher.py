from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.teacher import Teacher
from app.core.subjects import Subject
from app.schema.teacher import TeacherCreate, TeacherUpdate


def handle_teacher_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "email" in message:
        detail = "Email already exists"
    elif "teacher_code" in message:
        detail = "Teacher code already exists"
    else:
        detail = "Invalid teacher data"

    raise HTTPException(status_code=400, detail=detail)


def get_subjects_by_names(db: Session, subject_names: list[str]):
    subjects = db.query(Subject).filter(
        Subject.name.in_(subject_names)
    ).all()

    if len(subjects) != len(subject_names):
        raise HTTPException(
            status_code=404,
            detail="One or more subjects not found"
        )

    return subjects


def create_teacher(db: Session, teacher: TeacherCreate):
    subjects = get_subjects_by_names(db, teacher.subject_names)

    db_teacher = Teacher(
        teacher_code=teacher.teacher_code,
        name=teacher.name,
        age=teacher.age,
        gender=teacher.gender,
        father_name=teacher.father_name,
        dob=teacher.dob,
        mobile_number=teacher.mobile_number,
        email=teacher.email,
        department=teacher.department,
        subjects=subjects
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


def get_teacher_by_code(db: Session, teacher_code: str):
    return db.query(Teacher).filter(
        Teacher.teacher_code == teacher_code
    ).first()


def get_teacher_by_email(db: Session, email: str):
    return db.query(Teacher).filter(
        Teacher.email == email
    ).first()


def update_teacher_full(
    db: Session,
    teacher_code: str,
    teacher_data: TeacherCreate
):
    teacher = get_teacher_by_code(db, teacher_code)

    if teacher is None:
        return None

    subjects = get_subjects_by_names(db, teacher_data.subject_names)

    teacher.teacher_code = teacher_data.teacher_code
    teacher.name = teacher_data.name
    teacher.age = teacher_data.age
    teacher.gender = teacher_data.gender
    teacher.father_name = teacher_data.father_name
    teacher.dob = teacher_data.dob
    teacher.mobile_number = teacher_data.mobile_number
    teacher.email = teacher_data.email
    teacher.department = teacher_data.department
    teacher.subjects = subjects

    try:
        db.commit()
        db.refresh(teacher)
        return teacher
    except IntegrityError as error:
        db.rollback()
        handle_teacher_integrity_error(error)


def update_teacher_partial(
    db: Session,
    teacher_code: str,
    teacher_data: TeacherUpdate
):
    teacher = get_teacher_by_code(db, teacher_code)

    if teacher is None:
        return None

    update_data = teacher_data.model_dump(exclude_unset=True)

    if "subject_names" in update_data:
        subject_names = update_data.pop("subject_names")
        teacher.subjects = get_subjects_by_names(db, subject_names)

    for key, value in update_data.items():
        setattr(teacher, key, value)

    try:
        db.commit()
        db.refresh(teacher)
        return teacher
    except IntegrityError as error:
        db.rollback()
        handle_teacher_integrity_error(error)


def delete_teacher(db: Session, teacher_code: str):
    teacher = get_teacher_by_code(db, teacher_code)

    if teacher is None:
        return None

    db.delete(teacher)
    db.commit()

    return teacher
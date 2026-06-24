from uuid import UUID

from sqlalchemy.orm import Session

from app.core.teacher import Teacher
from app.schema.teacher import TeacherCreate, TeacherUpdate


def create_teacher(db: Session, teacher: TeacherCreate):
    db_teacher = Teacher(
        name=teacher.name,
        email=teacher.email,
        phone=teacher.phone,
        subject=teacher.subject,
        department=teacher.department
    )

    db.add(db_teacher)
    db.commit()
    db.refresh(db_teacher)

    return db_teacher


def get_teachers(db: Session):
    return db.query(Teacher).all()


def get_teacher_by_id(db: Session, teacher_id: UUID):
    return db.query(Teacher).filter(Teacher.id == teacher_id).first()

def get_teacher_by_email(db: Session, email: str):
    return db.query(Teacher).filter(Teacher.email == email).first()

def update_teacher_full(db: Session, teacher_id: UUID, teacher_data: TeacherCreate):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        return None

    teacher.name = teacher_data.name
    teacher.email = teacher_data.email
    teacher.phone = teacher_data.phone
    teacher.subject = teacher_data.subject
    teacher.department = teacher_data.department

    db.commit()
    db.refresh(teacher)

    return teacher


def update_teacher_partial(db: Session, teacher_id: UUID, teacher_data: TeacherUpdate):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        return None

    update_data = teacher_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(teacher, key, value)

    db.commit()
    db.refresh(teacher)

    return teacher


def delete_teacher(db: Session, teacher_id: UUID):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        return None

    db.delete(teacher)
    db.commit()

    return teacher
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.schedule import Schedule
from app.core.school_class import SchoolClass
from app.core.teacher import Teacher
from app.core.subjects import Subject
from app.schema.schedule import ScheduleCreate, ScheduleUpdate


def handle_schedule_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Class, teacher, or subject does not exist"
    else:
        detail = "Invalid schedule data"

    raise HTTPException(status_code=400, detail=detail)


def get_class_by_name_and_section(
    db: Session,
    class_name: int,
    section: str
):
    school_class = db.query(SchoolClass).filter(
        SchoolClass.name == class_name,
        SchoolClass.section == section
    ).first()

    if school_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return school_class


def get_teacher_by_code(db: Session, teacher_code: str):
    teacher = db.query(Teacher).filter(
        Teacher.teacher_code == teacher_code
    ).first()

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


def get_subject_by_name_and_class(
    db: Session,
    subject_name: str,
    class_name: int,
    section: str
):
    school_class = get_class_by_name_and_section(
        db,
        class_name,
        section
    )

    subject = db.query(Subject).filter(
        Subject.name == subject_name,
        Subject.class_id == school_class.id
    ).first()

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found in this class"
        )

    return subject


def create_schedule(db: Session, schedule: ScheduleCreate):
    school_class = get_class_by_name_and_section(
        db,
        schedule.class_name,
        schedule.section
    )

    teacher = get_teacher_by_code(
        db,
        schedule.teacher_code
    )

    subject = get_subject_by_name_and_class(
        db,
        schedule.subject_name,
        schedule.class_name,
        schedule.section
    )

    db_schedule = Schedule(
        class_id=school_class.id,
        teacher_id=teacher.id,
        subject_id=subject.id,
        day=schedule.day,
        start_time=schedule.start_time,
        end_time=schedule.end_time
    )

    db.add(db_schedule)

    try:
        db.commit()
        db.refresh(db_schedule)
        return db_schedule
    except IntegrityError as error:
        db.rollback()
        handle_schedule_integrity_error(error)


def get_schedules(db: Session):
    return db.query(Schedule).all()


def get_schedules_by_class_and_day(
    db: Session,
    class_name: int,
    section: str,
    day: str
):
    school_class = get_class_by_name_and_section(
        db,
        class_name,
        section
    )

    return db.query(Schedule).filter(
        Schedule.class_id == school_class.id,
        Schedule.day == day
    ).order_by(Schedule.start_time).all()


def get_schedule_by_class_day_start_time(
    db: Session,
    class_name: int,
    section: str,
    day: str,
    start_time
):
    school_class = get_class_by_name_and_section(
        db,
        class_name,
        section
    )

    return db.query(Schedule).filter(
        Schedule.class_id == school_class.id,
        Schedule.day == day,
        Schedule.start_time == start_time
    ).first()


def update_schedule_full(
    db: Session,
    class_name: int,
    section: str,
    day: str,
    start_time,
    schedule_data: ScheduleCreate
):
    schedule = get_schedule_by_class_day_start_time(
        db,
        class_name,
        section,
        day,
        start_time
    )

    if schedule is None:
        return None

    new_class = get_class_by_name_and_section(
        db,
        schedule_data.class_name,
        schedule_data.section
    )

    new_teacher = get_teacher_by_code(
        db,
        schedule_data.teacher_code
    )

    new_subject = get_subject_by_name_and_class(
        db,
        schedule_data.subject_name,
        schedule_data.class_name,
        schedule_data.section
    )

    schedule.class_id = new_class.id
    schedule.teacher_id = new_teacher.id
    schedule.subject_id = new_subject.id
    schedule.day = schedule_data.day
    schedule.start_time = schedule_data.start_time
    schedule.end_time = schedule_data.end_time

    try:
        db.commit()
        db.refresh(schedule)
        return schedule
    except IntegrityError as error:
        db.rollback()
        handle_schedule_integrity_error(error)


def update_schedule_partial(
    db: Session,
    class_name: int,
    section: str,
    day: str,
    start_time,
    schedule_data: ScheduleUpdate
):
    schedule = get_schedule_by_class_day_start_time(
        db,
        class_name,
        section,
        day,
        start_time
    )

    if schedule is None:
        return None

    update_data = schedule_data.model_dump(exclude_unset=True)

    new_class_name = update_data.pop("class_name", class_name)
    new_section = update_data.pop("section", section)

    if new_class_name != class_name or new_section != section:
        new_class = get_class_by_name_and_section(
            db,
            new_class_name,
            new_section
        )
        schedule.class_id = new_class.id

    if "teacher_code" in update_data:
        teacher_code = update_data.pop("teacher_code")
        teacher = get_teacher_by_code(db, teacher_code)
        schedule.teacher_id = teacher.id

    if "subject_name" in update_data:
        subject_name = update_data.pop("subject_name")
        subject = get_subject_by_name_and_class(
            db,
            subject_name,
            new_class_name,
            new_section
        )
        schedule.subject_id = subject.id

    for key, value in update_data.items():
        setattr(schedule, key, value)

    try:
        db.commit()
        db.refresh(schedule)
        return schedule
    except IntegrityError as error:
        db.rollback()
        handle_schedule_integrity_error(error)


def delete_schedule(
    db: Session,
    class_name: int,
    section: str,
    day: str,
    start_time
):
    schedule = get_schedule_by_class_day_start_time(
        db,
        class_name,
        section,
        day,
        start_time
    )

    if schedule is None:
        return None

    db.delete(schedule)
    db.commit()

    return schedule
    return schedule
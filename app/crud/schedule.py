from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.schedule import Schedule
from app.schema.schedule import ScheduleCreate, ScheduleUpdate


def handle_schedule_integrity_error(error: IntegrityError):
    message = str(error.orig)

    if "foreign key" in message or "ForeignKeyViolation" in message:
        detail = "Class or teacher does not exist"
    else:
        detail = "Invalid schedule data"

    raise HTTPException(
        status_code=400,
        detail=detail
    )


def create_schedule(db: Session, schedule: ScheduleCreate):
    db_schedule = Schedule(
        class_id=schedule.class_id,
        teacher_id=schedule.teacher_id,
        subject=schedule.subject,
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


def get_schedule_by_id(db: Session, schedule_id: UUID):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def update_schedule_full(
    db: Session,
    schedule_id: UUID,
    schedule_data: ScheduleCreate
):
    schedule = get_schedule_by_id(db, schedule_id)

    if schedule is None:
        return None

    schedule.class_id = schedule_data.class_id
    schedule.teacher_id = schedule_data.teacher_id
    schedule.subject = schedule_data.subject
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
    schedule_id: UUID,
    schedule_data: ScheduleUpdate
):
    schedule = get_schedule_by_id(db, schedule_id)

    if schedule is None:
        return None

    update_data = schedule_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(schedule, key, value)

    try:
        db.commit()
        db.refresh(schedule)
        return schedule
    except IntegrityError as error:
        db.rollback()
        handle_schedule_integrity_error(error)


def delete_schedule(db: Session, schedule_id: UUID):
    schedule = get_schedule_by_id(db, schedule_id)

    if schedule is None:
        return None

    db.delete(schedule)
    db.commit()

    return schedule
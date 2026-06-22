from sqlalchemy.orm import Session

from app.core.schedule import Schedule
from app.schema.schedule import ScheduleCreate, ScheduleUpdate


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
    db.commit()
    db.refresh(db_schedule)

    return db_schedule


def get_schedules(db: Session):
    return db.query(Schedule).all()


def get_schedule_by_id(db: Session, schedule_id: int):
    return db.query(Schedule).filter(Schedule.id == schedule_id).first()


def update_schedule_full(
    db: Session,
    schedule_id: int,
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

    db.commit()
    db.refresh(schedule)

    return schedule


def update_schedule_partial(
    db: Session,
    schedule_id: int,
    schedule_data: ScheduleUpdate
):
    schedule = get_schedule_by_id(db, schedule_id)

    if schedule is None:
        return None

    update_data = schedule_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(schedule, key, value)

    db.commit()
    db.refresh(schedule)

    return schedule


def delete_schedule(db: Session, schedule_id: int):
    schedule = get_schedule_by_id(db, schedule_id)

    if schedule is None:
        return None

    db.delete(schedule)
    db.commit()

    return schedule
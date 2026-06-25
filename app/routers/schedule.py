from datetime import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse
)
from app.crud.schedule import (
    create_schedule,
    get_schedules,
    get_schedules_by_class_and_day,
    get_schedule_by_class_day_start_time,
    update_schedule_full,
    update_schedule_partial,
    delete_schedule
)
from app.core.auth import require_roles


router = APIRouter(
    prefix="/schedules",
    tags=["Schedule"]
)


def build_schedule_response(schedule):
    return {
        "id": schedule.id,

        "class_name": schedule.school_class.name,
        "section": schedule.school_class.section,

        "teacher_name": schedule.teacher.name,
        "teacher_code": schedule.teacher.teacher_code,

        "subject_name": schedule.subject.name,

        "day": schedule.day,
        "start_time": schedule.start_time,
        "end_time": schedule.end_time,

        "created_at": schedule.created_at
    }


@router.post(
    "/",
    response_model=ScheduleResponse,
    status_code=status.HTTP_201_CREATED
)
def add_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["teacher", "admin"]))
):
    db_schedule = create_schedule(db, schedule)
    return build_schedule_response(db_schedule)


@router.get("/", response_model=list[ScheduleResponse])
def read_schedules(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["teacher", "admin"]))
):
    schedules = get_schedules(db)

    return [
        build_schedule_response(schedule)
        for schedule in schedules
    ]


@router.get(
    "/class/{class_name}/section/{section}/day/{day}",
    response_model=list[ScheduleResponse]
)
def read_schedules_by_class_and_day(
    class_name: int,
    section: str,
    day: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["student", "teacher", "admin"]))
):
    schedules = get_schedules_by_class_and_day(
        db,
        class_name,
        section,
        day
    )

    return [
        build_schedule_response(schedule)
        for schedule in schedules
    ]


@router.get(
    "/class/{class_name}/section/{section}/day/{day}/start/{start_time}",
    response_model=ScheduleResponse
)
def read_single_schedule(
    class_name: int,
    section: str,
    day: str,
    start_time: time,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["student", "teacher", "admin"]))
):
    schedule = get_schedule_by_class_day_start_time(
        db,
        class_name,
        section,
        day,
        start_time
    )

    if schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    return build_schedule_response(schedule)


@router.put(
    "/class/{class_name}/section/{section}/day/{day}/start/{start_time}",
    response_model=ScheduleResponse
)
def update_schedule_put(
    class_name: int,
    section: str,
    day: str,
    start_time: time,
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    updated_schedule = update_schedule_full(
        db,
        class_name,
        section,
        day,
        start_time,
        schedule_data
    )

    if updated_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    return build_schedule_response(updated_schedule)


@router.patch(
    "/class/{class_name}/section/{section}/day/{day}/start/{start_time}",
    response_model=ScheduleResponse
)
def update_schedule_patch(
    class_name: int,
    section: str,
    day: str,
    start_time: time,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    update_data = schedule_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )

    updated_schedule = update_schedule_partial(
        db,
        class_name,
        section,
        day,
        start_time,
        schedule_data
    )

    if updated_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    return build_schedule_response(updated_schedule)


@router.delete(
    "/class/{class_name}/section/{section}/day/{day}/start/{start_time}",
    status_code=status.HTTP_200_OK
)
def delete_schedule_route(
    class_name: int,
    section: str,
    day: str,
    start_time: time,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    deleted_schedule = delete_schedule(
        db,
        class_name,
        section,
        day,
        start_time
    )

    if deleted_schedule is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    return {
        "message": "Schedule deleted successfully"
    }
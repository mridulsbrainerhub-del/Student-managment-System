from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schema.schedule import (
    ScheduleCreate,
    ScheduleUpdate,
    ScheduleResponse
)
from app.crud.schedule import (
    create_schedule,
    get_schedules,
    get_schedule_by_id,
    update_schedule_full,
    update_schedule_partial,
    delete_schedule
)
from app.core.auth import get_current_user
from app.core.auth import require_roles


router = APIRouter(
    prefix="/schedules",
    tags=["Schedule"]
)


@router.post("/", response_model=ScheduleResponse)
def add_schedule(
    schedule: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["teacher","admin"]))
):
    return create_schedule(db, schedule)


@router.get("/", response_model=list[ScheduleResponse])
def read_schedules(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["teacher","admin"]))
):
    return get_schedules(db)


@router.get("/{schedule_id}", response_model=ScheduleResponse)
def read_schedule(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["teacher","admin"]))
):
    schedule = get_schedule_by_id(db, schedule_id)

    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return schedule


@router.put("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule_put(
    schedule_id: UUID,
    schedule_data: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    updated_schedule = update_schedule_full(db, schedule_id, schedule_data)

    if updated_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return updated_schedule


@router.patch("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule_patch(
    schedule_id: UUID,
    schedule_data: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    updated_schedule = update_schedule_partial(db, schedule_id, schedule_data)

    if updated_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return updated_schedule


@router.delete("/{schedule_id}")
def delete_schedule_route(
    schedule_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(["admin"]))
):
    deleted_schedule = delete_schedule(db, schedule_id)

    if deleted_schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")

    return {"message": "Schedule deleted successfully"}
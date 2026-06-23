from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schema.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from app.crud.teacher import (
    create_teacher,
    get_teachers,
    get_teacher_by_id,
    update_teacher_full,
    update_teacher_partial,
    delete_teacher
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)


@router.post("/", response_model=TeacherResponse)
def add_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return create_teacher(db, teacher)


@router.get("/", response_model=list[TeacherResponse])
def read_teachers(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    return get_teachers(db)


@router.get("/{teacher_id}", response_model=TeacherResponse)
def read_teacher(
    teacher_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    teacher = get_teacher_by_id(db, teacher_id)

    if teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return teacher


@router.put("/{teacher_id}", response_model=TeacherResponse)
def update_teacher_put(
    teacher_id: UUID,
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_teacher = update_teacher_full(db, teacher_id, teacher_data)

    if updated_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return updated_teacher


@router.patch("/{teacher_id}", response_model=TeacherResponse)
def update_teacher_patch(
    teacher_id: UUID,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    updated_teacher = update_teacher_partial(db, teacher_id, teacher_data)

    if updated_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return updated_teacher


@router.delete("/{teacher_id}")
def delete_teacher_route(
    teacher_id: UUID,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    deleted_teacher = delete_teacher(db, teacher_id)

    if deleted_teacher is None:
        raise HTTPException(status_code=404, detail="Teacher not found")

    return {"message": "Teacher data deleted successfully"}
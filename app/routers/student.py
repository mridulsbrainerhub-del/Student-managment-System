from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.student import StudentCreate, StudentResponse, StudentUpdate
from app.crud.student import (
    create_student,
    get_students,
    get_student_by_id,
    get_student_by_email,
    update_student_full,
    update_student_partial,
    delete_student
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_student(db, student)


@router.get("/", response_model=list[StudentResponse])
def read_students(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_students(db)


@router.get("/by-email", response_model=StudentResponse)
def read_student_by_email(
    email: EmailStr = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = get_student_by_email(db, email)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


@router.get("/{student_id}", response_model=StudentResponse)
def read_student(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return student


@router.put("/{student_id}", response_model=StudentResponse)
def update_student_put(
    student_id: UUID,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_student = update_student_full(db, student_id, student_data)

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return updated_student


@router.patch("/{student_id}", response_model=StudentResponse)
def update_student_patch(
    student_id: UUID,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    update_data = student_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )

    updated_student = update_student_partial(db, student_id, student_data)

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return updated_student


@router.delete("/{student_id}", status_code=status.HTTP_200_OK)
def delete_student_route(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_student = delete_student(db, student_id)

    if deleted_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return {
        "message": "Student data deleted successfully"
    }
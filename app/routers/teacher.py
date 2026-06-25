from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import EmailStr
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.teacher import TeacherCreate, TeacherUpdate, TeacherResponse
from app.crud.teacher import (
    create_teacher,
    get_teachers,
    get_teacher_by_code,
    get_teacher_by_email,
    update_teacher_full,
    update_teacher_partial,
    delete_teacher
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)


def build_teacher_response(teacher):
    return {
        "id": teacher.id,
        "teacher_code": teacher.teacher_code,
        "name": teacher.name,
        "age": teacher.age,
        "gender": teacher.gender,
        "father_name": teacher.father_name,
        "dob": teacher.dob,
        "mobile_number": teacher.mobile_number,
        "email": teacher.email,
        "department": teacher.department,
        "subject_names": [subject.name for subject in teacher.subjects],
        "created_at": teacher.created_at
    }


@router.post(
    "/",
    response_model=TeacherResponse,
    status_code=status.HTTP_201_CREATED
)
def add_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_teacher = create_teacher(db, teacher)
    return build_teacher_response(db_teacher)


@router.get("/", response_model=list[TeacherResponse])
def read_teachers(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    teachers = get_teachers(db)
    return [build_teacher_response(teacher) for teacher in teachers]


@router.get("/by-email", response_model=TeacherResponse)
def read_teacher_by_email(
    email: EmailStr = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    teacher = get_teacher_by_email(db, email)

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return build_teacher_response(teacher)


@router.get("/code/{teacher_code}", response_model=TeacherResponse)
def read_teacher_by_code(
    teacher_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    teacher = get_teacher_by_code(db, teacher_code)

    if teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return build_teacher_response(teacher)


@router.put("/code/{teacher_code}", response_model=TeacherResponse)
def update_teacher_put(
    teacher_code: str,
    teacher_data: TeacherCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_teacher = update_teacher_full(
        db,
        teacher_code,
        teacher_data
    )

    if updated_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return build_teacher_response(updated_teacher)


@router.patch("/code/{teacher_code}", response_model=TeacherResponse)
def update_teacher_patch(
    teacher_code: str,
    teacher_data: TeacherUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    update_data = teacher_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )

    updated_teacher = update_teacher_partial(
        db,
        teacher_code,
        teacher_data
    )

    if updated_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return build_teacher_response(updated_teacher)


@router.delete("/code/{teacher_code}", status_code=status.HTTP_200_OK)
def delete_teacher_route(
    teacher_code: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_teacher = delete_teacher(db, teacher_code)

    if deleted_teacher is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return {
        "message": "Teacher data deleted successfully"
    }
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.student import StudentCreate, StudentResponse, StudentUpdate
from app.crud.student import (
    create_student,
    get_students,
    get_student_by_email,
    get_student_by_roll_class_section,
    update_student_full,
    update_student_partial,
    delete_student
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


def build_student_response(student):
    return {
        "id": student.id,
        "full_name": student.full_name,
        "age": student.age,
        "gender": student.gender,
        "father_name": student.father_name,
        "dob": student.dob,
        "class_name": student.school_class.name if student.school_class else None,
        "section": student.school_class.section if student.school_class else None,
        "mobile_number": student.mobile_number,
        "email": student.email,
        "roll_number": student.roll_number,
        "address": student.address,
        "created_at": student.created_at
    }


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
    db_student = create_student(db, student)
    return build_student_response(db_student)


@router.get("/", response_model=list[StudentResponse])
def read_students(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    students = get_students(db)
    return [build_student_response(student) for student in students]


@router.get("/by-email", response_model=StudentResponse)
def read_student_by_email(
    email: str = Query(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = get_student_by_email(db, email)

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return build_student_response(student)


@router.get("/class/{class_name}/section/{section}/roll/{roll_number}", response_model=StudentResponse)
def read_student_by_class_section_roll(
    class_name: int,
    section: str,
    roll_number: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = get_student_by_roll_class_section(
        db,
        roll_number,
        class_name,
        section
    )

    if student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return build_student_response(student)


@router.put("/class/{class_name}/section/{section}/roll/{roll_number}", response_model=StudentResponse)
def update_student_put(
    class_name: int,
    section: str,
    roll_number: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_student = update_student_full(
        db,
        roll_number,
        class_name,
        section,
        student_data
    )

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return build_student_response(updated_student)


@router.patch("/class/{class_name}/section/{section}/roll/{roll_number}", response_model=StudentResponse)
def update_student_patch(
    class_name: int,
    section: str,
    roll_number: int,
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

    updated_student = update_student_partial(
        db,
        roll_number,
        class_name,
        section,
        student_data
    )

    if updated_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return build_student_response(updated_student)


@router.delete("/class/{class_name}/section/{section}/roll/{roll_number}", status_code=status.HTTP_200_OK)
def delete_student_route(
    class_name: int,
    section: str,
    roll_number: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_student = delete_student(
        db,
        roll_number,
        class_name,
        section
    )

    if deleted_student is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    return {
        "message": "Student data deleted successfully"
    }
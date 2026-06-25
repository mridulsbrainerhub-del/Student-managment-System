from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.grades import GradeCreate, GradeUpdate, GradeResponse
from app.crud.grades import (
    create_grade,
    get_grade_by_id,
    get_grades_by_student_email,
    update_grade,
    delete_grade
)
from app.core.users import User
from app.core.auth import require_roles


router = APIRouter(
    prefix="/grades",
    tags=["Grades"]
)


@router.post("/", response_model=GradeResponse)
def add_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    return create_grade(db, grade)


@router.get("/student/by-email/{email}")
def get_student_grades(
    email: str,
    db: Session = Depends(get_db)
):
    result = get_grades_by_student_email(db, email)

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student = result["student"]
    grades = result["grades"]

    return {
        "student_name": student.name,
        "student_email": student.email,
        "roll_number": student.roll_number,
        "class_id": student.class_id,
        "grades": grades
    }


@router.get("/{grade_id}", response_model=GradeResponse)
def get_single_grade(
    grade_id: UUID,
    db: Session = Depends(get_db)
):
    grade = get_grade_by_id(db, grade_id)

    if not grade:
        raise HTTPException(
            status_code=404,
            detail="Grade not found"
        )

    return grade


@router.put("/{grade_id}", response_model=GradeResponse)
def update_student_grade(
    grade_id: UUID,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    updated_grade = update_grade(db, grade_id, grade_data)

    if not updated_grade:
        raise HTTPException(
            status_code=404,
            detail="Grade not found"
        )

    return updated_grade


@router.delete("/{grade_id}")
def delete_student_grade(
    grade_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    deleted_grade = delete_grade(db, grade_id)

    if not deleted_grade:
        raise HTTPException(
            status_code=404,
            detail="Grade not found"
        )

    return {
        "message": "Grade deleted successfully"
    }
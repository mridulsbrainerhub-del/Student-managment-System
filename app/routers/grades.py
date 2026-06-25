from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.grades import GradeCreate, GradeUpdate, GradeResponse
from app.crud.grades import (
    create_grade,
    get_grades_by_student,
    get_grade_by_student_and_subject,
    update_grade,
    delete_grade
)
from app.core.users import User
from app.core.auth import require_roles


router = APIRouter(
    prefix="/grades",
    tags=["Grades"]
)


def build_grade_response(grade):
    return {
        "id": grade.id,

        "student_name": grade.student.full_name,
        "student_roll_number": grade.student.roll_number,

        "class_name": grade.student.school_class.name,
        "section": grade.student.school_class.section,

        "subject_name": grade.subject.name,

        "marks": grade.marks,
        "total_marks": grade.total_marks,
        "percentage": round((grade.marks / grade.total_marks) * 100, 2),

        "created_at": grade.created_at
    }


@router.post(
    "/",
    response_model=GradeResponse,
    status_code=status.HTTP_201_CREATED
)
def add_grade(
    grade: GradeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    db_grade = create_grade(db, grade)
    return build_grade_response(db_grade)


@router.get(
    "/class/{class_name}/section/{section}/roll/{roll_number}",
    response_model=list[GradeResponse]
)
def get_student_grades(
    class_name: int,
    section: str,
    roll_number: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["student", "teacher", "admin"]))
):
    grades = get_grades_by_student(
        db,
        roll_number,
        class_name,
        section
    )

    return [build_grade_response(grade) for grade in grades]


@router.get(
    "/class/{class_name}/section/{section}/roll/{roll_number}/subject/{subject_name}",
    response_model=GradeResponse
)
def get_single_grade(
    class_name: int,
    section: str,
    roll_number: int,
    subject_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["student", "teacher", "admin"]))
):
    grade = get_grade_by_student_and_subject(
        db,
        roll_number,
        class_name,
        section,
        subject_name
    )

    if grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    return build_grade_response(grade)


@router.put(
    "/class/{class_name}/section/{section}/roll/{roll_number}/subject/{subject_name}",
    response_model=GradeResponse
)
def update_student_grade_full(
    class_name: int,
    section: str,
    roll_number: int,
    subject_name: str,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    updated_grade = update_grade(
        db,
        roll_number,
        class_name,
        section,
        subject_name,
        grade_data
    )

    if updated_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    return build_grade_response(updated_grade)



@router.patch(
    "/class/{class_name}/section/{section}/roll/{roll_number}/subject/{subject_name}",
    response_model=GradeResponse
)
def update_student_grade_partial(
    class_name: int,
    section: str,
    roll_number: int,
    subject_name: str,
    grade_data: GradeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    update_data = grade_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )

    updated_grade = update_grade(
        db,
        roll_number,
        class_name,
        section,
        subject_name,
        grade_data
    )

    if updated_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    return build_grade_response(updated_grade)


@router.delete(
    "/class/{class_name}/section/{section}/roll/{roll_number}/subject/{subject_name}",
    status_code=status.HTTP_200_OK
)
def delete_student_grade(
    class_name: int,
    section: str,
    roll_number: int,
    subject_name: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["teacher", "admin"]))
):
    deleted_grade = delete_grade(
        db,
        roll_number,
        class_name,
        section,
        subject_name
    )

    if deleted_grade is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Grade not found"
        )

    return {
        "message": "Grade deleted successfully"
    }
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.schema.school_class import (
    SchoolClassCreate,
    SchoolClassUpdate,
    SchoolClassResponse
)
from app.crud.school_class import (
    create_school_class,
    get_school_classes,
    get_school_class_by_name_section,
    update_school_class_full,
    update_school_class_partial,
    delete_school_class
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)


def build_class_response(school_class):
    return {
        "id": school_class.id,

        "name": school_class.name,
        "section": school_class.section,
        "room_number": school_class.room_number,
        "batch_year": school_class.batch_year,

        "incharge_teacher_name": (
            school_class.incharge_teacher.name
            if school_class.incharge_teacher
            else None
        ),
        "incharge_teacher_code": (
            school_class.incharge_teacher.teacher_code
            if school_class.incharge_teacher
            else None
        ),
        "incharge_teacher_phone": (
            school_class.incharge_teacher.mobile_number
            if school_class.incharge_teacher
            else None
        ),

        "total_students": len(school_class.students),
        "subjects": [subject.name for subject in school_class.subjects],

        "created_at": school_class.created_at
    }


@router.post(
    "/",
    response_model=SchoolClassResponse,
    status_code=status.HTTP_201_CREATED
)
def add_school_class(
    school_class: SchoolClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    db_school_class = create_school_class(db, school_class)
    return build_class_response(db_school_class)


@router.get("/", response_model=list[SchoolClassResponse])
def read_school_classes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    classes = get_school_classes(db)

    return [
        build_class_response(school_class)
        for school_class in classes
    ]


@router.get(
    "/name/{name}/section/{section}",
    response_model=SchoolClassResponse
)
def read_school_class_by_name_section(
    name: int,
    section: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    school_class = get_school_class_by_name_section(
        db,
        name,
        section
    )

    if school_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return build_class_response(school_class)


@router.put(
    "/name/{name}/section/{section}",
    response_model=SchoolClassResponse
)
def update_school_class_put(
    name: int,
    section: str,
    class_data: SchoolClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_class = update_school_class_full(
        db,
        name,
        section,
        class_data
    )

    if updated_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return build_class_response(updated_class)


@router.patch(
    "/name/{name}/section/{section}",
    response_model=SchoolClassResponse
)
def update_school_class_patch(
    name: int,
    section: str,
    class_data: SchoolClassUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    update_data = class_data.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No data provided for update"
        )

    updated_class = update_school_class_partial(
        db,
        name,
        section,
        class_data
    )

    if updated_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return build_class_response(updated_class)


@router.delete(
    "/name/{name}/section/{section}",
    status_code=status.HTTP_200_OK
)
def delete_school_class_route(
    name: int,
    section: str,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_class = delete_school_class(
        db,
        name,
        section
    )

    if deleted_class is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Class not found"
        )

    return {
        "message": "Class data deleted successfully"
    }
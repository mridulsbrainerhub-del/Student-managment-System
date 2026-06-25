from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.schema.subjects import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse
)

from app.crud.subjects import (
    create_subject,
    get_subjects,
    get_subjects_by_class_name,
    get_subject_by_class_and_name,
    update_subject_by_class_and_name,
    delete_subject_by_class_and_name,
)


router = APIRouter(
    prefix="/subjects",
    tags=["Subjects"]
)


@router.post("/", response_model=SubjectResponse)
def add_subject(
    subject: SubjectCreate,
    db: Session = Depends(get_db)
):
    new_subject = create_subject(db, subject)

    if new_subject is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    return new_subject


@router.get("/", response_model=List[SubjectResponse])
def read_subjects(
    db: Session = Depends(get_db)
):
    return get_subjects(db)


@router.get("/class/{class_name}", response_model=List[SubjectResponse])
def read_subjects_by_class_name(
    class_name: str,
    db: Session = Depends(get_db)
):
    subjects = get_subjects_by_class_name(db, class_name)

    if subjects is None:
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    return subjects


@router.get("/{class_name}/{subject_name}", response_model=SubjectResponse)
def read_subject_by_class_and_name(
    class_name: str,
    subject_name: str,
    db: Session = Depends(get_db)
):
    subject = get_subject_by_class_and_name(
        db,
        class_name,
        subject_name
    )

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found for this class"
        )

    return subject


@router.put("/{class_name}/{subject_name}", response_model=SubjectResponse)
def edit_subject_by_class_and_name(
    class_name: str,
    subject_name: str,
    subject_update: SubjectUpdate,
    db: Session = Depends(get_db)
):
    subject = update_subject_by_class_and_name(
        db,
        class_name,
        subject_name,
        subject_update
    )

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found for this class"
        )

    return subject


@router.delete("/{class_name}/{subject_name}")
def remove_subject_by_class_and_name(
    class_name: str,
    subject_name: str,
    db: Session = Depends(get_db)
):
    subject = delete_subject_by_class_and_name(
        db,
        class_name,
        subject_name
    )

    if subject is None:
        raise HTTPException(
            status_code=404,
            detail="Subject not found for this class"
        )

    return {
        "message": "Subject deleted successfully"
    }
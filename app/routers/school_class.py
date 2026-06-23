from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.database import get_db
from app.schema.school_class import (
    SchoolClassCreate,
    SchoolClassUpdate,
    SchoolClassResponse
)
from app.crud.school_class import (
    create_school_class,
    get_school_classes,
    get_school_class_by_id,
    update_school_class_full,
    update_school_class_partial,
    delete_school_class
)
from app.core.auth import get_current_user


router = APIRouter(
    prefix="/classes",
    tags=["Classes"]
)


@router.post("/", response_model=SchoolClassResponse)
def add_school_class(
    school_class: SchoolClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_school_class(db, school_class)


@router.get("/", response_model=list[SchoolClassResponse])
def read_school_classes(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_school_classes(db)


@router.get("/{class_id}", response_model=SchoolClassResponse)
def read_school_class(
    class_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    school_class = get_school_class_by_id(db, class_id)

    if school_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return school_class


@router.put("/{class_id}", response_model=SchoolClassResponse)
def update_school_class_put(
    class_id: UUID,
    class_data: SchoolClassCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_class = update_school_class_full(db, class_id, class_data)

    if updated_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return updated_class


@router.patch("/{class_id}", response_model=SchoolClassResponse)
def update_school_class_patch(
    class_id: UUID,
    class_data: SchoolClassUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_class = update_school_class_partial(db, class_id, class_data)

    if updated_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return updated_class


@router.delete("/{class_id}")
def delete_school_class_route(
    class_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_class = delete_school_class(db, class_id)

    if deleted_class is None:
        raise HTTPException(status_code=404, detail="Class not found")

    return {"message": "Class data deleted successfully"}
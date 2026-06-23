from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.database.database import get_db
from app.schema.student import StudentCreate, StudentResponse,StudentUpdate
from app.crud.student import create_student,get_students,get_student_by_id,update_student_full,update_student_partial,delete_student
from app.core.auth import get_current_user






router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# endpoint for posting student data 
@router.post("/", response_model=StudentResponse)
def add_student(
    student: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return create_student(db, student)


# endpoint for getting all the data of the student
@router.get("/", response_model=list[StudentResponse])
def read_students(db: Session = Depends(get_db),current_user=Depends(get_current_user)):

    return get_students(db)




# endpoint for getting particular student data 
@router.get("/{student_id}", response_model=StudentResponse)
def read_student(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    student = get_student_by_id(db, student_id)

    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return student



# updating data of student  
@router.put("/{student_id}", response_model=StudentResponse)
def update_student_put(
    student_id: UUID,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_student = update_student_full(db, student_id, student_data)

    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student


# updating particular data of the student 
@router.patch("/{student_id}", response_model=StudentResponse)
def update_student_patch(
    student_id: UUID,
    student_data: StudentUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    updated_student = update_student_partial(db, student_id, student_data)

    if updated_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student




# endpoint to delete student 
@router.delete("/{student_id}")
def delete_student_route(
    student_id: UUID,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    deleted_student = delete_student(db, student_id)

    if deleted_student is None:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message":"student data deleted successfully."} 
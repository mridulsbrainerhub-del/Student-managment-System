from sqlalchemy.orm import Session

from app.core.student import Student
from app.schema.student import StudentCreate,StudentUpdate




# post student data 
def create_student(db: Session, student: StudentCreate):
    db_student = Student(
        name=student.name,
        email=student.email,
        phone=student.phone,
        age=student.age,
        roll_number=student.roll_number,
        class_name=student.class_name,
        address=student.address
    )

    db.add(db_student)
    db.commit()
    db.refresh(db_student)

    return db_student


# get student data 
def get_students(db:Session):
    return db.query(Student).all()

# get particular student data 
def get_student_by_id(db:Session,student_id:int):
    return db.query(Student).filter(Student.id==student_id).first()


# put operation 
def update_student_full(db: Session, student_id: int, student_data: StudentCreate):
    student = get_student_by_id(db, student_id)

    if student is None:
        return None

    student.name = student_data.name
    student.email = student_data.email
    student.phone = student_data.phone
    student.age = student_data.age
    student.roll_number = student_data.roll_number
    student.class_name = student_data.class_name
    student.address = student_data.address

    db.commit()
    db.refresh(student)

    return student


# patch operation 
def update_student_partial(db: Session, student_id: int, student_data: StudentUpdate):
    student = get_student_by_id(db, student_id)

    if student is None:
        return None

    update_data = student_data.model_dump(
        exclude_unset=True,
        exclude_none=True
    )

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student

# delete student by id 
def delete_student(db: Session, student_id: int):
    student = get_student_by_id(db, student_id)

    if student is None:
        return None

    db.delete(student)
    db.commit()

    return student
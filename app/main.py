from fastapi import FastAPI

from app.database.database import Base, engine
from app.core import student,users,teacher,school_class,schedule

from app.routers.student import router as student_router
from app.routers.auth import router as auth_router
from app.routers.teacher import router as teacher_router
from app.routers.school_class import router as school_class_router
from app.routers.schedule import router as schedule_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Study Buddy Club")


app.include_router(auth_router)
app.include_router(student_router)
app.include_router(teacher_router)
app.include_router(schedule_router)
app.include_router(school_class_router)
@app.get("/")
def home():
    return {"message": "Student Management System API is running"}
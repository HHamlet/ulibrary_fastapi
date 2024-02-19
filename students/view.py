from fastapi import APIRouter
from models.showmodels import ShowStudent
import students.crud as crud
from students.shemas import CreateStudentModel

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[ShowStudent])
async def get_students_list():
    return await crud.get_students_list()


@router.get("/student", response_model=ShowStudent)
async def get_student(first_name, last_name):
    return await crud.get_student(first_name, last_name)


@router.get("/{student_id}", response_model=ShowStudent)
async def get_student_by_id(student_id):
    return await crud.get_student_by_id(student_id)


@router.post("/registration")
async def student_registration(student: CreateStudentModel):
    return await crud.student_registration(student)


@router.post("/{student_id}")
async def delete_student_entity(student_id):
    return await crud.delete_student_entity(student_id)

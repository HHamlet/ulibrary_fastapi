from sqlalchemy import select
from books.crud import get_request
from db import async_session
from models.student import StudentModel
from students.shemas import CreateStudentModel


async def get_students_list():
    statement = select(StudentModel)
    result = await get_request(statement)
    return result


async def get_student(first_name, last_name):
    statement = select(StudentModel).where(
        StudentModel.first_name == first_name, StudentModel.last_name == last_name
    )
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
    return result


async def get_student_by_id(student_id):
    statement = select(StudentModel).where(StudentModel.id == int(student_id))
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
    return result


async def student_registration(student: CreateStudentModel):
    temp_student = await get_student(
        first_name=student.first_name, last_name=student.last_name
    )
    print("STUDENT_TEMP:", temp_student)
    if temp_student is None:
        student_statement = StudentModel(
            first_name=student.first_name,
            last_name=student.last_name,
            email=student.email,
        )
        async with async_session() as session:
            async with session.begin():
                session.add(student_statement)
                session.commit()
        return {"message": "student registration is done!"}
    else:
        return {"message": "student already exist..."}

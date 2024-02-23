from sqlalchemy import select
import helper
from db import async_session
from models.student import StudentModel
from students.shemas import CreateStudentModel


async def get_students_list():
    statement = select(StudentModel)
    result = await helper.get_request_all(statement)
    return result


async def get_student(first_name, last_name):
    statement = select(StudentModel).where(
        StudentModel.first_name == first_name, StudentModel.last_name == last_name
    )
    result = await helper.get_request_one(statement)
    return result


async def get_student_by_id(student_id):
    statement = select(StudentModel).where(StudentModel.id == int(student_id))
    result = await helper.get_request_one(statement)
    return result


async def student_registration(student: CreateStudentModel):
    temp_student = await get_student(
        first_name=student.first_name, last_name=student.last_name
    )
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


async def delete_student_entity(student_id):
    del_statement = select(StudentModel).where(StudentModel.id == student_id)
    async with async_session() as session:
        async with session.begin():
            session.delete(del_statement)
            session.commit()

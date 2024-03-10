from pydantic import BaseModel, EmailStr


class CreateStudentModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr


class ShowStudent(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

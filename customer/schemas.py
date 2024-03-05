from pydantic import BaseModel, EmailStr


class CreateCustomerModel(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    address: str | None = ""
    phone_number: str | None = ""

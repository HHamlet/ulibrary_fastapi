from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import BaseModel


class CustomerModel(BaseModel):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    first_name: Mapped[str] = mapped_column(String(50))
    last_name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50))

    def __repr__(self):
        return (
            f"CustomerModel(id: {self.id}, Customer: {self.first_name} {self.last_name}, "
            f"address : {self.address}, phone number : {self.phone_number})"
        )

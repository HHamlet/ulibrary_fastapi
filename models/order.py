import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.customer import CustomerModel
from models.base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped[CustomerModel] = relationship(lazy="joined")
    book_list: Mapped[str]
    order_data: Mapped[datetime.date]
    total_price: Mapped[int]

    def __repr__(self):
        return (
            f"OrderModel(id={self.id},Customer: {self.customer} Order item :{self.book_list}, "
            f"Ordered : {self.order_data}, total : {self.total_price})"
        )

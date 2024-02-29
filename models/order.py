import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.order_item import OrderItemModel
from models.customer import CustomerModel
from models.base import BaseModel


class OrderModel(BaseModel):
    __tablename__ = "order"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey("order_item.id"))
    order_item: Mapped[OrderItemModel] = relationship(lazy="joined")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    customer: Mapped[CustomerModel] = relationship(lazy="joined")
    order_data: Mapped[datetime.date]
    total: Mapped[int]
    shipping: Mapped[bool]

    def __repr__(self):
        return (
            f"OrderModel(id={self.id},Customer: {self.customer} Order item :{self.order_item}, "
            f"Ordered : {self.order_data}, total : {self.total}, shipped : {self.shipping})"
        )

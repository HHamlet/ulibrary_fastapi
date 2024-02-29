from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.book_copies import Book_CopiesModel
from .base import BaseModel


class OrderItemModel(BaseModel):
    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    book_copies_id: Mapped[int] = mapped_column(ForeignKey("book_copies.id"))
    book_copies: Mapped[Book_CopiesModel] = relationship(lazy="joined")
    quantity: Mapped[int]
    item_price: Mapped[int]

    def __repr__(self):
        return f"OrderItemModel(id={self.id}, Item : {self.book_copies_id})"

import datetime
import json
from sqlalchemy import select
from db import async_session
from models import OrderItemModel, Book_CopiesModel, OrderModel
from models.customer import CustomerModel
from customer.schemas import CreateCustomerModel
import helper


async def get_customer(first_name, last_name):
    statement = select(CustomerModel).where(
        CustomerModel.first_name == first_name, CustomerModel.last_name == last_name
    )
    result = await helper.get_request_one(statement)
    return result


async def get_customer_by_id(customer_id):
    statement = select(CustomerModel).where(CustomerModel.id == int(customer_id))
    result = await helper.get_request_one(statement)
    return result


async def create_customer_entity(customer: CreateCustomerModel):
    customer_res = await get_customer(customer.first_name, customer.last_name)
    async with async_session() as session:
        async with session.begin():
            if customer_res is None:
                statement_customer = CustomerModel(
                    first_name=customer.first_name,
                    last_name=customer.last_name,
                    email=customer.email,
                    address=customer.address,
                    phone_number=customer.phone_number,
                )
                session.add(statement_customer)
                session.commit()


async def add_to_cart(customer_id, book_copy_id):
    order_item = OrderItemModel(
        book_copies_id=int(book_copy_id), customer_id=int(customer_id)
    )
    async with async_session() as session:
        async with session.begin():
            session.add(order_item)
            session.commit()


async def del_from_cart(item_id):
    del_statement = select(OrderItemModel).where(OrderItemModel.id == item_id)
    async with async_session() as session:
        async with session.begin():
            session.delete(del_statement)
            session.commit()


async def buy(customer_id):
    item_dict = {}
    statement = select(OrderItemModel).where(OrderItemModel.customer_id == customer_id)
    item_list = await helper.get_request_all(statement)
    total_price = 0
    for ind in range(len(item_list)):
        book_item = item_list[ind]
        item_dict[ind + 1] = book_item
        book_statement = select(Book_CopiesModel).where(
            Book_CopiesModel.id == book_item
        )
        result = await helper.get_request_one(book_statement)
        total_price += result.price
    json_str = json.dumps(item_dict)

    order = OrderModel(
        customer_id=customer_id,
        book_list=json_str,
        order_data=datetime.datetime.today(),
        total_price=total_price,
    )
    async with async_session() as session:
        async with session.begin():
            session.add(order)
            for ind in range(len(item_list)):
                del_statement = select(Book_CopiesModel).where(
                    Book_CopiesModel.id == ind
                )
                session.delete(del_statement)
            session.commit()

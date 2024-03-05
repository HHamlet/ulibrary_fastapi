from fastapi import APIRouter
from customer import crud
from customer.schemas import CreateCustomerModel
from models.showmodels import ShowBooksCopy

router = APIRouter(prefix="/customer", tags=["Customer"])


@router.get("/{id}")
async def get_customer_by_id(customer_id):
    return await crud.get_customer_by_id(customer_id)


@router.post("/add_customer")
async def create_customer_entity(customer: CreateCustomerModel):
    return await crud.create_customer_entity(customer)


@router.post("/{customer_id}/add_cart")
async def add_to_cart(customer_id, book_copy_id):
    return await crud.add_to_cart(customer_id, book_copy_id)


@router.get("/{isbn}", response_model=list[ShowBooksCopy])
async def get_by_isbn(isbn: str):
    return await crud.get_by_isbn(isbn)

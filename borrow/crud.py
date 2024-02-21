import datetime
from sqlalchemy import select
from db import async_session
from models import BorrowsModel, Book_CopiesModel, StudentModel
from books.crud import get_request


async def check_book_in_borrow_table(book_copy_id):
    statement = select(BorrowsModel).where(
        BorrowsModel.book_copies_id == int(book_copy_id)
    )
    async with async_session() as session:
        async with session.begin():
            temp = await session.scalars(statement)
            result = temp.first()
        if result is not None:
            return {"message": "book already borrowed"}
    return {"message": "book available for sign to ..."}


async def student_taken_books(student_id):
    statement = select(BorrowsModel).where(BorrowsModel.student_id == int(student_id))
    result = await get_request(statement)
    return result


async def borrow_to(book_copy_id, student_id):
    book = None
    student = None
    if await check_book_in_borrow_table(book_copy_id) is False:
        book = select(Book_CopiesModel).where(Book_CopiesModel.id == book_copy_id)

    if len(await student_taken_books(student_id)) < 5:
        student = select(StudentModel).where(StudentModel.id == student_id)

    if book is not None and student is not None:
        async with async_session() as session:
            async with session.begin():
                book_to_sign = session.scalars(book).first()
                sign_to_student = session.scalars(student).first()
                statement_borrow = BorrowsModel(
                    book_copies_id=book_to_sign.id,
                    student_id=sign_to_student.id,
                    borrowed_data=datetime.date.today(),
                )
                statement_borrow.return_data = (
                    statement_borrow.borrowed_data + datetime.timedelta(14)
                )
                session.add(statement_borrow)
                session.commit()
                return {"message": "book signed..."}
    else:
        return {"message": "book or student are not available"}

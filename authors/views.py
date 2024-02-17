from fastapi import APIRouter
import authors.crud as crud
from models.showmodels import ShowAuthor

router = APIRouter(prefix="/authors", tags=["Authors"])


@router.get("/", response_model=ShowAuthor)
async def get_author(name, lastname):
    return await crud.get_author(name, lastname)

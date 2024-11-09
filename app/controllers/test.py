from fastapi import APIRouter
from app.repositories.test import get_test
from app.dtos.test import Test
from app.services.db import DB


router = APIRouter(
    prefix='/api/test',
    tags=['Test']
)


@router.get("/connection")
async def read_root(db: DB):
    return {"message": "Connected to MySQL"}


@router.get("/", response_model=list[Test])
def read_test(db: DB):
    test = get_test(db)
    return test
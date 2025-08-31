from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy import select, update, delete, insert
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.models.human import HumanStorage
from service.db.connection import get_session
from pydantic import UUID4
from service.schemas.human_response import HumanResponse, ListHumanResponse
from typing import List
from sqlalchemy.exc import DBAPIError


api_router = APIRouter(tags=["Insert data"])


@api_router.post(
    path="/insert_data",
    response_class=JSONResponse
)
async def insert_data(
        id: int,
        name: str,
        age: int,
        gender: str,
        session: AsyncSession = Depends(get_session)
):
    new_human = HumanStorage(id=id, name=name, age=age, gender=gender)
    try:
        session.add(new_human)
        await session.commit()
    except DBAPIError:
        return {"status": "current id already exist"}
    return {"status": "ok"}

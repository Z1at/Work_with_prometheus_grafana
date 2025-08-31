from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.models.human import HumanStorage
from service.db.connection import get_session
from service.schemas.human_response import HumanResponse, ListHumanResponse
from typing import List


api_router = APIRouter(tags=["Get data"])


@api_router.get(
    path="/get_data_by_id",
    response_model=list[HumanResponse]
)
async def get_data_by_id(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    db_human_query = select(HumanStorage).where(HumanStorage.id == id).with_for_update()
    db_human = await session.scalars(db_human_query)

    return db_human.all()

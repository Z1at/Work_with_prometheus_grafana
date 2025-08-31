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
    path="/get_all_data",
    response_model=list[HumanResponse]
)
async def get_all_data(
        session: AsyncSession = Depends(get_session)
):
    db_human_query = select(HumanStorage).with_for_update()
    db_human = await session.scalars(db_human_query)

    return db_human.all()

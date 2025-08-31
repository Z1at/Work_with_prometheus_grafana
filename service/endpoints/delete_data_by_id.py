from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.models.human import HumanStorage
from service.db.connection import get_session
from pydantic import UUID4
from service.schemas.human_response import HumanResponse, ListHumanResponse
from typing import List


api_router = APIRouter(tags=["Delete data"])


@api_router.delete(
    path="/delete_data_by_id",
    response_class=JSONResponse
)
async def delete_data_by_id(
        id: int,
        session: AsyncSession = Depends(get_session)
):
    db_human_query = select(HumanStorage).where(HumanStorage.id == id)
    db_human = await session.scalar(db_human_query)

    if db_human:
        await session.delete(db_human)
        await session.commit()
        return {"status": "ok"}
    return {"status": "user not found"}

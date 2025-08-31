from fastapi import APIRouter, Depends, HTTPException, Path, Request
from fastapi.responses import PlainTextResponse, JSONResponse
from sqlalchemy import select, update, delete, insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from service.db.models.human import HumanStorage
from service.db.connection import get_session
from pydantic import UUID4
from service.schemas.human_response import HumanResponse, ListHumanResponse
from typing import List
from sqlalchemy.exc import DBAPIError


api_router = APIRouter(tags=["Run query"])


@api_router.post(
    path="/run_query",
    response_class=PlainTextResponse
)
async def run_query(
        query: str,
        session: AsyncSession = Depends(get_session)
):
    query_text = text(query)

    try:
        result = await session.execute(query_text)

        rows = result.fetchall()

        if not rows:
            return "Query executed successfully, but no rows were returned."

        header = " | ".join(result.keys())

        separator = "-+-".join(["-" * len(col) for col in result.keys()])

        formatted_rows = [header, separator]
        for row in rows:
            formatted_rows.append(" | ".join(str(item) for item in row))

        return "\n".join(formatted_rows)

    except DBAPIError as e:
        await session.rollback()
        return f"Database error: {e}"
    except Exception:
        try:
            await session.commit()
            return "Query executed successfully (no rows returned or changes committed)."
        except Exception as e:
            return f"An unexpected error occurred: {e}"

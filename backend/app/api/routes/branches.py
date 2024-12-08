import uuid
from typing import Any, List  # noqa: UP035

from fastapi import APIRouter, HTTPException
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.core.db import database
from app.models import Message

router = APIRouter()


@router.get("/")
def read_items(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve items.
    """

    return {}


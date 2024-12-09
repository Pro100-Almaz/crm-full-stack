import uuid
from typing import Any

from fastapi import APIRouter

from app.api.deps import CurrentUser
from app.core.db import database

router = APIRouter()


@router.get("/")
def read_items(
    current_user: CurrentUser
) -> Any:
    """
    Retrieve items.
    """

    return {}


import json
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.api.deps import CurrentUser, require_auth
from app.api.schemas import Branch
from app.core.db import database


router = APIRouter()


@router.get("/")
async def read_rooms():
    rooms = await database.fetch(
        """
            SELECT *
            FROM public.room
        """
    )

    return {"Status": 200, "rooms": rooms}


@router.get("/{room_id}")
async def read_room(room_id: int):
    room = await database.fetchrow(
        """
            SELECT *
            FROM public.room
            WHERE id = $1
        """, room_id
    )

    return {"Status": 200, "room": room}


@router.post("/")
@require_auth
async def create_branch(
    *, room_name: str, branch_id: uuid.UUID
) -> Any:
    try:
        room = await database.fetchrow(
            """
                INSERT INTO public.room (name, branch_id)
                VALUES ($1, $2)
                RETURNING id;
            """, room_name, branch_id
        )

        return {"Status": "success", "status_code": 201, "room": room.get('id')}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Insertion error")


@router.patch("/")
@require_auth
async def update_room(
    room_id: int, room_name: str | None = None, branch_id: uuid.UUID | None = None
) -> Any:
    if room_name is None and branch_id is None:
        return {"Status": "Error", "details": "Must specify either room_name or branch_id", "status_code": 400}

    try :
        query_string = """
                        UPDATE public.room
                        SET 
                       """

        query_variables = [room_id]
        query_index = 2

        if room_name:
            query_variables.append(room_name)
            query_string += f"room = ${query_index}, "
            query_index += 1

        if branch_id:
            query_variables.append(branch_id)
            query_string += f"branch = ${query_index}"

        query_string += "\nWHERE id = $1;"

        await database.execute(query_string, *query_variables)
        return {"Status": "success", "status_code": 201}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error updating room")


@router.delete("/{room_id}")
@require_auth
async def delete_room(room_id: int) -> Any:
    try:
        await database.execute(
            """
                DELETE FROM public.room
                WHERE id = $1;
            """, room_id
        )

        return {"Status": "success", "status_code": 200}

    except Exception as e:
        raise HTTPException(status_code=400, detail="Error deleting room")

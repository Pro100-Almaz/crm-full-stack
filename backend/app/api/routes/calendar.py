import json
import uuid
from datetime import datetime
from typing import Any, List, Optional  # noqa: UP035

from fastapi import APIRouter, HTTPException, Query, status

from app.api.deps import CurrentUser, require_auth
from app.api.schemas import EventCreate, EventUpdate
from app.core.db import database

router = APIRouter()


async def check_overlapping_event(start_time: datetime, end_time: datetime, event_id: int | None = None) -> bool:
    query = """
        SELECT 1 FROM calendar.events
        WHERE start_time < $2 AND end_time > $1
    """
    params = [start_time, end_time]
    if event_id:
        query += " AND id != $3"
        params.append(event_id)

    result = await database.fetchrow(query, *params)
    return result is not None


async def get_events_query(
    user_id,
    skip: int = 0,
    limit: int = 100,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    title: str | None = None,
    sort_by: str = "start_time",
) -> list[dict]:
    base_query = "SELECT id, title, description, start_time, end_time, user_id, room FROM calendar.events"
    conditions = []
    values = []
    counter = 1

    if start_date:
        conditions.append(f"start_time >= ${counter}")
        values.append(start_date)
        counter += 1
    if end_date:
        conditions.append(f"end_time <= ${counter}")
        values.append(end_date)
        counter += 1
    if title:
        conditions.append(f"title ILIKE '%' || ${counter} || '%'")
        values.append(title)
        counter += 1

    conditions.append(f"user_id = ${counter}")
    values.append(user_id)
    counter += 1

    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    if sort_by not in ["start_time", "end_time", "title"]:
        sort_by = "start_time"

    base_query += f" ORDER BY {sort_by} ASC LIMIT ${counter} OFFSET ${counter+1}"
    values.extend([limit, skip])

    return await database.fetch(base_query, *values)


async def update_event_query(event_id: int, event: EventUpdate) -> dict | None:
    fields = []
    values = []
    counter = 1
    for field, value in event.model_dump(exclude_unset=True).items():
        fields.append(f"{field} = ${counter}")
        values.append(value)
        counter +=1
    if not fields:
        return await get_event(event_id)  # Nothing to update

    set_clause = ", ".join(fields)
    query = (f"UPDATE calendar.events SET {set_clause} WHERE id = ${counter} "
             f"RETURNING id, title, description, start_time, end_time, user_id, room;")
    values.append(event_id)
    return await database.fetchrow(query, *values)


@router.post("/events/", status_code=status.HTTP_201_CREATED)
async def create_event(event: EventCreate, current_user: CurrentUser):
    if event.end_time <= event.start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )

    overlap = await check_overlapping_event(event.start_time, event.end_time)
    if overlap:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Event times overlap with an existing event."
        )

    room_id = await database.fetchrow(
        """
            SELECT 1
            FROM public.room
            WHERE id = $1
        """, event.room
    )

    if not room_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No such room id.",
        )

    user_id = event.user_id if event.user_id else current_user.id

    new_event = await database.execute(
        """
            INSERT INTO calendar.events (title, description, start_time, end_time, user_id, room)
            VALUES ($1, $2, $3, $4, $5, $6)
            RETURNING id, title, description, start_time, end_time, user_id, room;
        """, event.title, event.description, event.start_time, event.end_time, user_id, event.room
    )
    return new_event


@router.get("/events/")
async def get_events(
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = Query(100, le=100),
    start_date: datetime | None = Query(
        None, description="Filter events starting from this date"
    ),
    end_date: datetime | None = Query(
        None, description="Filter events up to this date"
    ),
    title: str | None = Query(None, description="Search by title"),
    sort_by: str = Query("start_time", description="Sort by field")
):
    events = await get_events_query(
        skip=skip,
        limit=limit,
        start_date=start_date,
        end_date=end_date,
        title=title,
        sort_by=sort_by,
        user_id=current_user.id
    )

    return events


@router.get("/events/{event_id}")
async def get_event(event_id: int):
    event = await database.fetchrow(
        """
            SELECT *
            FROM calendar.events
            WHERE id = $1
        """, event_id
    )

    if not event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found."
        )
    return event


@router.put("/events/{event_id}")
@require_auth
async def update_event(event_id: int, event_update: EventUpdate):
    existing_event = await database.fetchrow(
        """
            SELECT 1
            FROM calendar.events
            WHERE id = $1
        """, event_id
    )

    if not existing_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found."
        )

    new_start_time = event_update.start_time or existing_event["start_time"]
    new_end_time = event_update.end_time or existing_event["end_time"]
    if new_end_time <= new_start_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End time must be after start time.",
        )

    overlap = await check_overlapping_event(
        new_start_time, new_end_time, event_id=event_id
    )
    if overlap:
        raise ValueError("Event times overlap with an existing event.")

    updated_event = await update_event_query(event_id, event_update)
    return updated_event


@router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def api_delete_event(event_id: int, current_user: CurrentUser):
    existing_event = await database.fetchrow(
        """
            SELECT 1
            FROM calendar.events
            WHERE id = $1 AND user_id = $2;
        """, event_id, current_user.id
    )

    if not existing_event:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found."
        )

    success = await database.execute("DELETE FROM calendar.events WHERE id = $1;", event_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete event.",
        )

    return

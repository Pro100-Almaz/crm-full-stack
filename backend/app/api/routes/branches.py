import json
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException

from app.api.deps import CurrentUser
from app.api.schemas import Branch
from app.core.db import database

router = APIRouter()


@router.get("/")
async def read_branches() -> Any:
    branches = await database.fetch(
        """
            SELECT *
            FROM public.branch
        """
    )

    return branches


@router.post("/")
async def create_branch(
    *, branch: Branch, current_user: CurrentUser
) -> Any:
    has_authority = await database.fetchrow(
        """
            SELECT branch_add
            FROM public.role
            WHERE id = (
                SELECT job_role
                FROM public.user
                WHERE id = $1
            )
        """, current_user.id
    )

    if has_authority:
        if not branch.group_id or branch.group_id == "string":
            group_id = await database.fetchrow(
                """
                    SELECT id
                    FROM public.branchgroup
                    WHERE name = 'Основной';
                """
            )

            branch.group_id = group_id["id"]

        try:
            uuid4 = uuid.uuid4()

            await database.execute(
                """
                    INSERT INTO public.branch (id, name, internal_name, abbreviation, address, newsletter_address, address_note,
                                               time_zone, group_id, workdays, holidays, work_hours, 
                                               responsible_user_for_authomative_actions, display_color, send_notification)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);
                """, uuid4, branch.name, branch.internal_name, branch.abbreviation, branch.address, branch.newsletter_address,
                branch.address_note, branch.time_zone, branch.group_id, branch.workdays, branch.holidays, branch.work_hours,
                branch.responsible_for_aa, branch.display_color, json.dumps(branch.send_notification)
            )

            return {"Status": "success", "status_code": 201}

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Insertion error")

    raise HTTPException(status_code=403, detail="Forbidden, has no enough authority")


@router.patch("/")
async def update_branch(
    *, branch: Branch, current_user: CurrentUser
) -> Any:
    has_authority = await database.fetchrow(
        """
            SELECT branch_add
            FROM public.role
            WHERE id = (
                SELECT job_role
                FROM public.user
                WHERE id = $1
            )
        """, current_user.id
    )

    if has_authority:
        if not branch.group_id or branch.group_id == "string":
            group_id = await database.fetchrow(
                """
                    SELECT id
                    FROM public.branchgroup
                    WHERE name = 'Основной';
                """
            )

            branch.group_id = group_id["id"]

        try:
            uuid4 = uuid.uuid4()

            await database.execute(
                """
                    INSERT INTO public.branch (id, name, internal_name, abbreviation, address, newsletter_address, address_note,
                                               time_zone, group_id, workdays, holidays, work_hours, 
                                               responsible_user_for_authomative_actions, display_color, send_notification)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15);
                """, uuid4, branch.name, branch.internal_name, branch.abbreviation, branch.address, branch.newsletter_address,
                branch.address_note, branch.time_zone, branch.group_id, branch.workdays, branch.holidays, branch.work_hours,
                branch.responsible_for_aa, branch.display_color, json.dumps(branch.send_notification)
            )

            return {"Status": "success", "status_code": 201}

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Insertion error")

    raise HTTPException(status_code=403, detail="Forbidden, has no enough authority")

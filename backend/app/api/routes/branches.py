import json
import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from app.api.deps import CurrentUser
from app.api.schemas import Branch
from app.core.db import database

router = APIRouter()


@router.get("/")
async def read_branches():
    branches = await database.fetch(
        """
            SELECT *
            FROM public.branch
        """
    )

    return {"Status": 200, "branches": branches}


@router.get("/{branch_id}")
async def read_branch(branch_id: uuid.UUID):
    branch = await database.fetchrow(
        """
            SELECT *
            FROM public.branch
            WHERE id = $1
        """, branch_id
    )

    return {"Status": 200, "branch": branch}


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
            raise HTTPException(status_code=400, detail="Insertion error")

    raise HTTPException(status_code=403, detail="Forbidden, has no enough authority")


@router.patch("/")
async def update_branch(
    *, branch: Branch, current_user: CurrentUser
) -> Any:
    has_authority = await database.fetchrow(
        """
            SELECT branch_update
            FROM public.role
            WHERE id = (
                SELECT job_role
                FROM public.user
                WHERE id = $1
            )
        """, current_user.id
    )

    if has_authority:
        if not branch.id or branch.id == "string":
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail="Branch id is not provided"
            )

        try:
            query_string = """
                UPDATE public.branch
                SET 
            """

            query_variables = []
            parameter_index = 2

            for value in branch:
                if value[1]:
                    if value[0] == 'responsible_for_aa':
                        query_string += f"responsible_user_for_authomative_actions = ${parameter_index}, "
                    else:
                        query_string += f"{value[0]} = ${parameter_index}, "

                    query_variables.append(value[1])
                    parameter_index += 1

            query_string = query_string.rstrip(", ")

            query_string += "\nWHERE id = $1;"

            query_variables.insert(0, branch.id)

            try:
                await database.execute(query_string, *query_variables)
            except Exception as e:
                return {"Status": "error", "message": "Error updating branch"}

            return {"Status": "success", "status_code": 201}

        except Exception as e:
            print(e)
            raise HTTPException(status_code=400, detail="Insertion error")

    raise HTTPException(status_code=403, detail="Forbidden, has no enough authority")


@router.delete("/")
async def delete_branch(
    branch_id: uuid.UUID, current_user: CurrentUser
) -> Any:
    has_authority = await database.fetchrow(
        """
            SELECT branch_update
            FROM public.role
            WHERE id = (
                SELECT job_role
                FROM public.user
                WHERE id = $1
            )
        """,
        current_user.id,
    )

    if has_authority:
        try:
            await database.execute(
                """
                    DELETE FROM public.branch
                    WHERE id = $1;
                """, branch_id
            )

            return {"Status": "success", "status_code": 204, "message": "Branch deleted"}
        except Exception:
            raise HTTPException(status_code=400, detail="Insertion error")
    else:
        raise HTTPException(status_code=403, detail="Forbidden, has no enough authority")

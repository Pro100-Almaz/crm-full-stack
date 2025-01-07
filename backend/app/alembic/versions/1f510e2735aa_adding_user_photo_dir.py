"""Adding user photo dir

Revision ID: 1f510e2735aa
Revises: e9912789c8ca
Create Date: 2025-01-07 19:43:04.259892

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '1f510e2735aa'
down_revision = 'e9912789c8ca'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            ALTER TABLE public.user 
            ADD COLUMN photo VARCHAR(255) DEFAULT 'default.jpg';
        """
    )


def downgrade():
    pass

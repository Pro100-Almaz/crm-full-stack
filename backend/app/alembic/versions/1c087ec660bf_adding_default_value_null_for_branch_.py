"""Adding default value null for branch column

Revision ID: 1c087ec660bf
Revises: 018f920c63aa
Create Date: 2024-12-17 18:59:21.427709

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c087ec660bf'
down_revision = '018f920c63aa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
            ALTER TABLE public.branch
            ALTER COLUMN responsible_user_for_authomative_actions DROP NOT NULL;
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
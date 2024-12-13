"""Added new table room

Revision ID: cdc403441f62
Revises: acde65016c89
Create Date: 2024-12-13 18:54:50.857874

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'cdc403441f62'
down_revision = 'acde65016c89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
            CREATE TABLE room (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                branch_id FO
            );
    """)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###

    # ### end Alembic commands ###
"""Added new table holiday

Revision ID: acde65016c89
Revises: 0d91a6e072df
Create Date: 2024-12-13 18:44:32.492574

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'acde65016c89'
down_revision = '0d91a6e072df'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute("""
            CREATE TABLE holiday (
                id SERIAL PRIMARY KEY,
                date TIMESTAMP WITH TIME ZONE NOT NULL,
                name VARCHAR(255) NOT NULL,
                is_recurring BOOLEAN NOT NULL DEFAULT FALSE
            );
    """)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('holiday')
    # ### end Alembic commands ###
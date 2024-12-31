"""Adding calendar table

Revision ID: b9dcd885d897
Revises: 1c087ec660bf
Create Date: 2024-12-31 15:16:27.397464

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'b9dcd885d897'
down_revision = '1c087ec660bf'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.execute(
        """
            CREATE SCHEMA calendar;
        """
    )
    op.execute(
        """
            CREATE TABLE calendar.events (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                start_time TIMESTAMP NOT NULL,
                end_time TIMESTAMP NOT NULL,
                user_id UUID,
                FOREIGN KEY (user_id) REFERENCES public.user(id) ON DELETE CASCADE,
                room INTEGER,
                FOREIGN KEY (room) REFERENCES public.room(id) ON DELETE CASCADE
            );
        """
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('calendar.events')
    # ### end Alembic commands ###

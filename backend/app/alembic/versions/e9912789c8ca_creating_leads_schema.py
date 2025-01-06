"""Creating leads schema

Revision ID: e9912789c8ca
Revises: 8516ca36a195
Create Date: 2025-01-06 21:44:13.923445

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'e9912789c8ca'
down_revision = '8516ca36a195'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        """
            CREATE SCHEMA leads;
        """
    )

    op.execute(
        """
            CREATE TABLE leads.client_status(
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                number INT GENERATED ALWAYS AS IDENTITY
            );
        """
    )

    op.execute(
        """
            INSERT INTO leads.client_status (name) VALUES ('cold');
        """
    )

    op.execute(
        """
            INSERT INTO leads.client_status (name) VALUES ('warm');
        """
    )

    op.execute(
        """
            INSERT INTO leads.client_status (name) VALUES ('hot');
        """
    )

    op.execute(
        """
            CREATE TABLE leads.clients(
                id SERIAL PRIMARY KEY,
                name VARCHAR(255),
                phone VARCHAR(10),
                email VARCHAR(100),
                source VARCHAR(255),
                created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description TEXT,
                category VARCHAR(255),
                interests VARCHAR(255),
                status INT NOT NULL DEFAULT 1,
                FOREIGN KEY (status) REFERENCES leads.client_status (id),
                responsible_manager UUID NOT NULL,
                FOREIGN KEY (responsible_manager) REFERENCES public.user (id)
            );
        """
    )


def downgrade():
    op.execute(
        """
            DROP SCHEMA leads CASCADE;
        """
    )

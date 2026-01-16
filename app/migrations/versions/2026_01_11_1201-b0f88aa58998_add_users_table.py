"""add users table

Revision ID: b0f88aa58998
Revises: b07dba3632b3
Create Date: 2026-01-11 12:01:39.628373

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b0f88aa58998"
down_revision: Union[str, Sequence[str], None] = "b07dba3632b3"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("users")

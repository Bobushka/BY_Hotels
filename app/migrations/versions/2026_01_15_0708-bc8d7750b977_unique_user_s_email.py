"""unique user's email

Revision ID: bc8d7750b977
Revises: b0f88aa58998
Create Date: 2026-01-15 07:08:43.944003

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc8d7750b977"
down_revision: Union[str, Sequence[str], None] = "b0f88aa58998"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")

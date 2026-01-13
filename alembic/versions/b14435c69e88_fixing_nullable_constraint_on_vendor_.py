"""Fixing nullable constraint on vendor_items.ingredient_id

Revision ID: b14435c69e88
Revises: c365506839cb
Create Date: 2026-01-13 16:16:17.172801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b14435c69e88'
down_revision: Union[str, Sequence[str], None] = 'c365506839cb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("vendor_items") as batch_op:
        batch_op.alter_column(
            "ingredient_id",
            existing_type=sa.Integer(),
            nullable=True
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("vendor_items") as batch_op:
        batch_op.alter_column(
            "ingredient_id",
            existing_type=sa.Integer(),
            nullable=False
        )

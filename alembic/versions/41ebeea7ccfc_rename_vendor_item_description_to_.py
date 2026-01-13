"""Rename vendor_item.description to vendor_item.vendor_description

Revision ID: 41ebeea7ccfc
Revises: 22d968893a32
Create Date: 2026-01-13 13:44:34.072444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41ebeea7ccfc'
down_revision: Union[str, Sequence[str], None] = '22d968893a32'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "vendor_items",
        "description",
        new_column_name="vendor_description"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "vendor_items",
        "vendor_description",
        new_column_name="description"
    )

"""Changing 'vendor_items.pack_size' to 'vendor_items.purchase_unit'

Revision ID: c365506839cb
Revises: 41ebeea7ccfc
Create Date: 2026-01-13 15:56:47.632801

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c365506839cb'
down_revision: Union[str, Sequence[str], None] = '41ebeea7ccfc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "vendor_items",
        "pack_size",
        new_column_name="purchase_unit"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "vendor_items",
        "purchase_unit",
        new_column_name="pack_size"
    )

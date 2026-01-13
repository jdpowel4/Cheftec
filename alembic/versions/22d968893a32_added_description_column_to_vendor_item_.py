"""Added Description Column to Vendor Item table

Revision ID: 22d968893a32
Revises: b5e7dadc8942
Create Date: 2026-01-13 13:13:37.903353

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22d968893a32'
down_revision: Union[str, Sequence[str], None] = 'b5e7dadc8942'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "vendor_items",
        sa.Column("description", sa.String(), nullable=True)
    )
    


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("vendor_items", "description")
    

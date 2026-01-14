"""Added provisions for Idempotency (ensuring invoices can't be duplicated)

Revision ID: cba24c5efbf6
Revises: b14435c69e88
Create Date: 2026-01-13 19:16:14.323416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cba24c5efbf6'
down_revision: Union[str, Sequence[str], None] = 'b14435c69e88'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table("invoices", recreate="always") as batch_op:
        batch_op.create_unique_constraint(
            "uq_vendor_invoice",
            ["vendor_id", "invoice_number"]
        )


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table("invoices", recreate="always") as batch_op:
        batch_op.drop_constraint(
            "uq_vendor_invoice",
            type_="unique"
        )
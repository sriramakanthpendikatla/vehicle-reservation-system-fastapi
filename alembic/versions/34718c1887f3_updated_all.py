"""updated all

Revision ID: 34718c1887f3
Revises: 1db08be3d6fb
Create Date: 2026-06-02 17:13:22.020926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34718c1887f3'
down_revision: Union[str, Sequence[str], None] = '1db08be3d6fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

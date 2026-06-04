"""merge heads

Revision ID: cbb3df414018
Revises: 7a76f9d65876, da64ee015df0
Create Date: 2026-06-03 17:03:30.603508

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cbb3df414018'
down_revision: Union[str, Sequence[str], None] = ('7a76f9d65876', 'da64ee015df0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

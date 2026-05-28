"""merge 1473 and c3a1

Revision ID: ca33bef9b569
Revises: 1473d3d0b714, c3a1f3a9b7
Create Date: 2026-05-28 15:24:23.845909

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ca33bef9b569'
down_revision: Union[str, Sequence[str], None] = ('1473d3d0b714', 'c3a1f3a9b7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

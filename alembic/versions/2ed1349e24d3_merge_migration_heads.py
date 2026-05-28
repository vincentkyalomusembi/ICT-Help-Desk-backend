"""merge migration heads

Revision ID: 2ed1349e24d3
Revises: 120fc93bba2c, a6d489d75960
Create Date: 2026-05-28 14:35:55.844065

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ed1349e24d3'
down_revision: Union[str, Sequence[str], None] = ('120fc93bba2c', 'a6d489d75960')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

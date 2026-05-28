"""merge all heads

Revision ID: bbd09ba1c37d
Revises: 120fc93bba2c, b2000daaf0f8
Create Date: 2026-05-28 16:21:59.845539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bbd09ba1c37d'
down_revision: Union[str, Sequence[str], None] = ('120fc93bba2c', 'b2000daaf0f8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

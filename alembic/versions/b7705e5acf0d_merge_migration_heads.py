"""merge migration heads

Revision ID: b7705e5acf0d
Revises: ca33bef9b569, d2100fae1c2
Create Date: 2026-05-28 15:40:07.699483

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b7705e5acf0d'
down_revision: Union[str, Sequence[str], None] = ('ca33bef9b569', 'd2100fae1c2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

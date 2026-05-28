"""create ticket table

Revision ID: d2100fae1c2
Revises: 54fd007a10c1
Create Date: 2026-05-28 14:24:12.194052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
import sqlmodel

# revision identifiers, used by Alembic.
revision: str = 'd2100fae1c2'
down_revision: Union[str, Sequence[str], None] = '54fd007a10c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('tickets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('staff_id', sa.UUID(), nullable=False),
    sa.Column('assigned_to_id', sa.Integer(), nullable=True),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(length=150), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('category', sa.Enum('HARDWARE', 'SOFTWARE', 'NETWORK', 'ACCESS_PERMISSIONS', 'SECURITY_INCIDENTS', 'OTHER', name='ticketcategory'), nullable=False),
    sa.Column('status', sa.Enum('OPEN', 'IN_PROGRESS', 'RESOLVED', 'CLOSED', name='ticketstatus'), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('resolved_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['assigned_to_id'], ['ict_personnel.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.auth_user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('tickets')

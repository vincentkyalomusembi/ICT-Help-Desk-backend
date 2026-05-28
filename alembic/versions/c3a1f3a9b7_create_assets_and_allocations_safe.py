"""create assets and asset_allocations (safe)

Revision ID: c3a1f3a9b7
Revises: b2000daaf0f8
Create Date: 2026-05-28 15:30:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'c3a1f3a9b7'
down_revision: Union[str, Sequence[str], None] = 'b2000daaf0f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: create assets and asset_allocations if missing."""
    # create assets table
    op.create_table(
        'assets',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('asset_tag', sa.String(length=50), nullable=False),
        sa.Column('serial_number', sa.String(length=100), nullable=False),
        sa.Column('device_type', sa.String(length=50), nullable=False),
        sa.Column('brand', sa.String(length=50), nullable=False),
        sa.Column('condition', sa.String(length=50), nullable=False),
        sa.Column('purchase_date', sa.Date(), nullable=True),
        sa.Column('warranty_expiry_date', sa.Date(), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    op.create_index(op.f('ix_assets_asset_tag'), 'assets', ['asset_tag'], unique=True)
    op.create_index(op.f('ix_assets_serial_number'), 'assets', ['serial_number'], unique=True)

    # create asset_allocations table
    op.create_table(
        'asset_allocations',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('asset_id', sa.Integer(), nullable=False),
        sa.Column('staff_id', sa.UUID(), nullable=False),
        sa.Column('allocation_date', sa.Date(), nullable=False),
        sa.Column('return_date', sa.Date(), nullable=True),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id']),
    )


def downgrade() -> None:
    """Downgrade schema: drop created tables."""
    op.drop_table('asset_allocations')
    op.drop_index(op.f('ix_assets_serial_number'), table_name='assets')
    op.drop_index(op.f('ix_assets_asset_tag'), table_name='assets')
    op.drop_table('assets')

"""Add asset and asset allocation models

Revision ID: 339e52587ba3
Revises: 54fd007a10c1
Create Date: 2026-05-28 13:57:04.168582

"""
import sqlmodel
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '339e52587ba3'
down_revision: Union[str, Sequence[str], None] = '54fd007a10c1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE TYPE devicetype AS ENUM ('laptop', 'desktop', 'monitor', 'printer', 'other')")
    op.execute("CREATE TYPE brand AS ENUM ('dell', 'hp', 'lenovo', 'apple', 'asus', 'acer', 'huawei', 'other')")
    op.execute("CREATE TYPE assetcondition AS ENUM ('good', 'fair', 'poor', 'decommissioned')")

    op.create_table('assets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_tag', sqlmodel.sql.sqltypes.AutoString(length=50), nullable=False),
    sa.Column('serial_number', sqlmodel.sql.sqltypes.AutoString(length=100), nullable=False),
    sa.Column('device_type', postgresql.ENUM('laptop', 'desktop', 'monitor', 'printer', 'other', name='devicetype', create_type=False), nullable=False),
    sa.Column('brand', postgresql.ENUM('dell', 'hp', 'lenovo', 'apple', 'asus', 'acer', 'huawei', 'other', name='brand', create_type=False), nullable=False),
    sa.Column('condition', postgresql.ENUM('good', 'fair', 'poor', 'decommissioned', name='assetcondition', create_type=False), nullable=False),
    sa.Column('purchase_date', sa.Date(), nullable=True),
    sa.Column('warranty_expiry_date', sa.Date(), nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assets_asset_tag'), 'assets', ['asset_tag'], unique=True)
    op.create_index(op.f('ix_assets_serial_number'), 'assets', ['serial_number'], unique=True)
    op.create_table('asset_allocations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('asset_id', sa.Integer(), nullable=False),
    sa.Column('staff_id', sa.UUID(), nullable=False),
    sa.Column('allocation_date', sa.Date(), nullable=False),
    sa.Column('return_date', sa.Date(), nullable=True),
    sa.Column('notes', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_index(op.f('ix_audit_logs_action'), table_name='audit_logs', if_exists=True)
    op.drop_index(op.f('ix_audit_logs_table_name'), table_name='audit_logs', if_exists=True)
    op.drop_table('audit_logs', if_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.create_table('audit_logs',
    sa.Column('log_id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('staff_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('action', sa.VARCHAR(length=100), autoincrement=False, nullable=False),
    sa.Column('table_name', sa.VARCHAR(length=50), autoincrement=False, nullable=False),
    sa.Column('record_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('ip_address', sa.VARCHAR(length=45), autoincrement=False, nullable=True),
    sa.Column('mac_address', sa.VARCHAR(length=17), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), server_default=sa.text('now()'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['staff_id'], ['staff.auth_user_id'], name=op.f('audit_logs_staff_id_fkey')),
    sa.PrimaryKeyConstraint('log_id', name=op.f('audit_logs_pkey'))
    )
    op.create_index(op.f('ix_audit_logs_table_name'), 'audit_logs', ['table_name'], unique=False)
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.drop_table('asset_allocations')
    op.drop_index(op.f('ix_assets_serial_number'), table_name='assets')
    op.drop_index(op.f('ix_assets_asset_tag'), table_name='assets')
    op.drop_table('assets')
    op.execute("DROP TYPE IF EXISTS devicetype")
    op.execute("DROP TYPE IF EXISTS brand")
    op.execute("DROP TYPE IF EXISTS assetcondition")
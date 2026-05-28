"""
Audit service for logging all system actions.
Tracks user actions, system changes, and important events.
"""

from typing import Optional, List
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import uuid
from app.models.audit_logs import AuditLog, AuditAction


class AuditService:
    """Service for managing audit logs."""

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    async def log_action(
        self,
        action: AuditAction | str,
        table_name: str,
        staff_id: Optional[uuid.UUID] = None,
        record_id: Optional[int] = None,
        ip_address: Optional[str] = None,
        mac_address: Optional[str] = None,
    ) -> AuditLog:
        """
        Log an action to the audit table.

        Args:
            action: The action performed (e.g. TICKET_CREATED)
            table_name: Name of the affected table
            staff_id: ID of the user who performed the action (None for system actions)
            record_id: ID of the specific record that was affected
            ip_address: IP address of the user (for security tracking)

        Returns:
            The created AuditLog record
        """
        audit_log = AuditLog(
            staff_id=staff_id,
            action=str(action),
            table_name=table_name,
            record_id=record_id,
            ip_address=ip_address,
            mac_address=mac_address,
            created_at=datetime.utcnow(),
        )
        self.db.add(audit_log)
        await self.db.commit()
        await self.db.refresh(audit_log)
        return audit_log

    async def get_user_logs(
        self, staff_id: uuid.UUID, limit: int = 50
    ) -> List[AuditLog]:
        """
        Get all audit logs for a specific user.

        Args:
            staff_id: The staff member ID
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the user, ordered by most recent first
        """
        query = (
            select(AuditLog)
            .where(AuditLog.staff_id == staff_id)
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_table_logs(
        self, table_name: str, limit: int = 50
    ) -> List[AuditLog]:
        """
        Get all audit logs for changes to a specific table.

        Args:
            table_name: The database table name
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the table, ordered by most recent first
        """
        query = (
            select(AuditLog)
            .where(AuditLog.table_name == table_name)
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_record_logs(
        self, table_name: str, record_id: int
    ) -> List[AuditLog]:
        """
        Get all audit logs for changes to a specific record.

        Args:
            table_name: The database table name
            record_id: The record ID

        Returns:
            List of audit logs for the record, ordered by most recent first
        """
        query = (
            select(AuditLog)
            .where(
                (AuditLog.table_name == table_name)
                & (AuditLog.record_id == record_id)
            )
            .order_by(desc(AuditLog.created_at))
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_action_logs(
        self, action: AuditAction | str, limit: int = 50
    ) -> List[AuditLog]:
        """
        Get all audit logs for a specific action type.

        Args:
            action: The action type (e.g. TICKET_CREATED)
            limit: Maximum number of records to return

        Returns:
            List of audit logs for the action, ordered by most recent first
        """
        query = (
            select(AuditLog)
            .where(AuditLog.action == str(action))
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_recent_logs(self, limit: int = 50) -> List[AuditLog]:
        """
        Get the most recent audit logs across the entire system.

        Args:
            limit: Maximum number of records to return

        Returns:
            List of most recent audit logs
        """
        query = select(AuditLog).order_by(desc(AuditLog.created_at)).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_logs_by_date_range(
        self, start_date: datetime, end_date: datetime, limit: int = 500
    ) -> List[AuditLog]:
        """
        Get audit logs within a date range.

        Args:
            start_date: Start of date range
            end_date: End of date range
            limit: Maximum number of records to return

        Returns:
            List of audit logs within the date range
        """
        query = (
            select(AuditLog)
            .where(
                (AuditLog.created_at >= start_date)
                & (AuditLog.created_at <= end_date)
            )
            .order_by(desc(AuditLog.created_at))
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_login_failures(
        self, staff_id: Optional[uuid.UUID] = None, limit: int = 50
    ) -> List[AuditLog]:
        """
        Get failed login attempts, optionally filtered by user.

        Args:
            staff_id: Optional staff ID to filter by
            limit: Maximum number of records to return

        Returns:
            List of failed login audit logs
        """
        query = select(AuditLog).where(
            AuditLog.action == AuditAction.LOGIN_FAILED.value
        )
        if staff_id:
            query = query.where(AuditLog.staff_id == staff_id)
        query = query.order_by(desc(AuditLog.created_at)).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

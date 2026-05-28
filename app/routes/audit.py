"""
Audit log routes - endpoints for querying system audit logs.
"""

from fastapi import APIRouter, Depends, Query
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.db.database import get_session
from app.services.audit_service import AuditService
from app.models.audit_logs import AuditLogResponse

router = APIRouter(prefix="/api/audit", tags=["audit"])


@router.get("/logs/recent", response_model=list[AuditLogResponse])
async def get_recent_logs(
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_session),
):
    """Get the most recent audit logs."""
    service = AuditService(db)
    logs = await service.get_recent_logs(limit=limit)
    return logs


@router.get("/logs/user/{staff_id}", response_model=list[AuditLogResponse])
async def get_user_logs(
    staff_id: uuid.UUID,
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_session),
):
    """Get all audit logs for a specific user."""
    service = AuditService(db)
    logs = await service.get_user_logs(staff_id=staff_id, limit=limit)
    return logs


@router.get("/logs/table/{table_name}", response_model=list[AuditLogResponse])
async def get_table_logs(
    table_name: str,
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_session),
):
    """Get all audit logs for changes to a specific table."""
    service = AuditService(db)
    logs = await service.get_table_logs(table_name=table_name, limit=limit)
    return logs


@router.get(
    "/logs/record/{table_name}/{record_id}", response_model=list[AuditLogResponse]
)
async def get_record_logs(
    table_name: str,
    record_id: int,
    db: AsyncSession = Depends(get_session),
):
    """Get all audit logs for changes to a specific record."""
    service = AuditService(db)
    logs = await service.get_record_logs(table_name=table_name, record_id=record_id)
    return logs


@router.get("/logs/action/{action}", response_model=list[AuditLogResponse])
async def get_action_logs(
    action: str,
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_session),
):
    """Get all audit logs for a specific action type."""
    service = AuditService(db)
    logs = await service.get_action_logs(action=action, limit=limit)
    return logs


@router.get("/logs/date-range", response_model=list[AuditLogResponse])
async def get_logs_by_date_range(
    start_date: datetime,
    end_date: datetime,
    limit: int = Query(500, ge=1, le=5000),
    db: AsyncSession = Depends(get_session),
):
    """Get audit logs within a specific date range."""
    service = AuditService(db)
    logs = await service.get_logs_by_date_range(
        start_date=start_date, end_date=end_date, limit=limit
    )
    return logs


@router.get("/logs/login-failures", response_model=list[AuditLogResponse])
async def get_login_failures(
    staff_id: uuid.UUID | None = Query(None),
    limit: int = Query(50, ge=1, le=500),
    db: AsyncSession = Depends(get_session),
):
    """
    Get failed login attempts.
    Optionally filter by staff_id to see failures for a specific user.
    """
    service = AuditService(db)
    logs = await service.get_login_failures(staff_id=staff_id, limit=limit)
    return logs

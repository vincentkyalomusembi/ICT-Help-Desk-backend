from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.db.database import get_session
from app.core import supabase
from app.models import User, UserRole

bearer_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    session: AsyncSession = Depends(get_session)
) -> User:
    token = credentials.credentials

    try:
        response = supabase.auth.get_user(token)
        auth_user = response.user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    if not auth_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    
    result = await session.exec(
        select(User).where(User.auth_user_id == UUID(auth_user.id))
    )
    user = result.one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User profile not found"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account deactivated. Contact support."
        )

    if not user.is_activated:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account not activated. Check your email."
        )

    return user


async def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return current_user


async def require_staff(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff only"
        )
    return current_user


async def require_technician(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.technician:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Technicians only"
        )
    return current_user
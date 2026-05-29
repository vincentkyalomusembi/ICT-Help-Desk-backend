from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select

from app.models import Directorate, Department


class DirectorateService:

    async def get_all_directorates(
        self,
        session: AsyncSession
    ) -> list[Directorate]:
        result = await session.exec(select(Directorate))
        return result.all()

    async def get_departments_by_directorate(
        self,
        session: AsyncSession,
        directorate_id: int
    ) -> list[Department]:
        directorate = await session.get(Directorate, directorate_id)
        if not directorate:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Directorate not found"
            )
        result = await session.exec(
            select(Department).where(Department.directorate_id == directorate_id)
        )
        return result.all()
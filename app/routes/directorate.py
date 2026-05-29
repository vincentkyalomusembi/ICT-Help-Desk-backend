from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import get_session
from app.schemas import DirectorateResponse, DepartmentResponse
from app.services.directorate import DirectorateService

router = APIRouter(prefix="/directorates", tags=["Directorates"])

directorate_service = DirectorateService()


@router.get("/", response_model=list[DirectorateResponse])
async def get_all_directorates(
    session: AsyncSession = Depends(get_session)
):
    return await directorate_service.get_all_directorates(session)


@router.get("/{directorate_id}/departments", response_model=list[DepartmentResponse])
async def get_departments(
    directorate_id: int,
    session: AsyncSession = Depends(get_session)
):
    return await directorate_service.get_departments_by_directorate(session, directorate_id)
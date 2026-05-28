from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession

from app.db.database import get_session
from app.schemas import UserCreate, UserResponse, UserLogin, LoginResponse
from app.services import UserService

router = APIRouter(prefix="/auth", tags=["Auth"])

user_service = UserService()


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    payload: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    return await user_service.create_user(session, payload)


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: UserLogin,
    session: AsyncSession = Depends(get_session)
):
    return await user_service.login(session, payload.email, payload.password)

@router.post("/verify", response_model=UserResponse)
async def verify_account(
    token: str,
    session: AsyncSession = Depends(get_session)
):
    return await user_service.activate_account(session, token)
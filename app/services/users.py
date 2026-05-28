from fastapi import HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from uuid import UUID

from app.models import User, UserRole
from app.schemas import UserCreate, UserResponse
from app.core import supabase


class UserService:

    async def create_user(
        self,
        session: AsyncSession,
        payload: UserCreate
    ) -> User:

    
        result = await session.exec(
            select(User).where(User.personal_no == payload.personal_no)
        )
        existing = result.one_or_none()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Personal number already registered"
            )

        
        try:
            auth_response = supabase.auth.admin.create_user({
                "email": payload.email,
                "password": payload.password,
                "phone": payload.phone,
                "email_confirm": False  
            })
            auth_user = auth_response.user
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to create auth user: {str(e)}"
            )
        
        try:
            user = User(
                auth_user_id=UUID(auth_user.id),
                personal_no=payload.personal_no,
                first_name=payload.first_name,
                last_name=payload.last_name,
                directorate_id=payload.directorate_id,
                department_id=payload.department_id,
                office_number=payload.office_number,
                office_location=payload.office_location,
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

        except Exception as e:
        
            supabase.auth.admin.delete_user(auth_user.id)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to save user profile: {str(e)}"
            )
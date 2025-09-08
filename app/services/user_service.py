"""
User service for business logic
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.db.models import User, UserPlatform, UserPreferences
from app.schemas.user import (
    UserCreate, UserUpdate, UserPreferencesCreate, 
    UserPreferencesUpdate, UserPlatformCreate
)


class UserService:
    """User service for handling user-related operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        user = User(**user_data.model_dump())
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_user(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.platforms), selectinload(User.preferences))
            .where(User.id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_phone(self, phone: str) -> Optional[User]:
        """Get user by phone"""
        result = await self.db.execute(
            select(User).where(User.phone == phone)
        )
        return result.scalar_one_or_none()
    
    async def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information"""
        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_user(user_id)
        
        await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_user(user_id)
    
    async def delete_user(self, user_id: int) -> bool:
        """Soft delete user"""
        result = await self.db.execute(
            update(User)
            .where(User.id == user_id)
            .values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def add_user_platform(self, user_id: int, platform_data: UserPlatformCreate) -> Optional[UserPlatform]:
        """Add a platform account to user"""
        # Check if user exists
        user = await self.get_user(user_id)
        if not user:
            return None
        
        user_platform = UserPlatform(
            user_id=user_id,
            **platform_data.model_dump()
        )
        self.db.add(user_platform)
        await self.db.commit()
        await self.db.refresh(user_platform)
        return user_platform
    
    async def get_user_platforms(self, user_id: int) -> List[UserPlatform]:
        """Get user's platform accounts"""
        result = await self.db.execute(
            select(UserPlatform).where(UserPlatform.user_id == user_id)
        )
        return result.scalars().all()
    
    async def create_user_preferences(self, user_id: int, preferences_data: UserPreferencesCreate) -> Optional[UserPreferences]:
        """Create user preferences"""
        # Check if user exists
        user = await self.get_user(user_id)
        if not user:
            return None
        
        user_preferences = UserPreferences(
            user_id=user_id,
            **preferences_data.model_dump()
        )
        self.db.add(user_preferences)
        await self.db.commit()
        await self.db.refresh(user_preferences)
        return user_preferences
    
    async def get_user_preferences(self, user_id: int) -> Optional[UserPreferences]:
        """Get user preferences"""
        result = await self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def update_user_preferences(self, user_id: int, preferences_update: UserPreferencesUpdate) -> Optional[UserPreferences]:
        """Update user preferences"""
        update_data = preferences_update.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_user_preferences(user_id)
        
        await self.db.execute(
            update(UserPreferences)
            .where(UserPreferences.user_id == user_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_user_preferences(user_id)
    
    async def get_user_by_platform(self, platform: str, platform_user_id: str) -> Optional[User]:
        """Get user by platform and platform user ID"""
        result = await self.db.execute(
            select(User)
            .join(UserPlatform)
            .where(
                UserPlatform.platform == platform,
                UserPlatform.platform_user_id == platform_user_id
            )
        )
        return result.scalar_one_or_none()
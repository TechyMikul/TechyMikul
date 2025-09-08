"""
User management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.schemas.user import (
    UserCreate, UserResponse, UserUpdate, 
    UserPreferencesCreate, UserPreferencesResponse, UserPreferencesUpdate,
    UserPlatformCreate, UserPlatformResponse
)
from app.services.user_service import UserService

router = APIRouter()


@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new user"""
    user_service = UserService(db)
    return await user_service.create_user(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user by ID"""
    user_service = UserService(db)
    user = await user_service.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update user information"""
    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete user (soft delete)"""
    user_service = UserService(db)
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return {"message": "User deleted successfully"}


@router.post("/{user_id}/platforms", response_model=UserPlatformResponse)
async def add_user_platform(
    user_id: int,
    platform: UserPlatformCreate,
    db: AsyncSession = Depends(get_db)
):
    """Add a platform account to user"""
    user_service = UserService(db)
    user_platform = await user_service.add_user_platform(user_id, platform)
    if not user_platform:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_platform


@router.get("/{user_id}/platforms", response_model=List[UserPlatformResponse])
async def get_user_platforms(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user's platform accounts"""
    user_service = UserService(db)
    platforms = await user_service.get_user_platforms(user_id)
    return platforms


@router.post("/{user_id}/preferences", response_model=UserPreferencesResponse)
async def create_user_preferences(
    user_id: int,
    preferences: UserPreferencesCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create user preferences"""
    user_service = UserService(db)
    user_preferences = await user_service.create_user_preferences(user_id, preferences)
    if not user_preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user_preferences


@router.get("/{user_id}/preferences", response_model=UserPreferencesResponse)
async def get_user_preferences(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user preferences"""
    user_service = UserService(db)
    preferences = await user_service.get_user_preferences(user_id)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found"
        )
    return preferences


@router.put("/{user_id}/preferences", response_model=UserPreferencesResponse)
async def update_user_preferences(
    user_id: int,
    preferences_update: UserPreferencesUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update user preferences"""
    user_service = UserService(db)
    preferences = await user_service.update_user_preferences(user_id, preferences_update)
    if not preferences:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found"
        )
    return preferences
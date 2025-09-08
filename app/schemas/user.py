"""
User-related Pydantic schemas
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from app.db.models import UserType, Platform


class UserBase(BaseModel):
    """Base user schema"""
    first_name: str
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    user_type: UserType
    language: str = "en"


class UserCreate(UserBase):
    """Schema for creating a user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating a user"""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    language: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserPlatformCreate(BaseModel):
    """Schema for creating user platform account"""
    platform: Platform
    platform_user_id: str
    username: Optional[str] = None


class UserPlatformResponse(BaseModel):
    """Schema for user platform response"""
    id: int
    platform: Platform
    platform_user_id: str
    username: Optional[str] = None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class UserPreferencesCreate(BaseModel):
    """Schema for creating user preferences"""
    interests: List[str] = []
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    budget_range: Optional[str] = None
    notification_frequency: str = "daily"


class UserPreferencesUpdate(BaseModel):
    """Schema for updating user preferences"""
    interests: Optional[List[str]] = None
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    budget_range: Optional[str] = None
    notification_frequency: Optional[str] = None


class UserPreferencesResponse(BaseModel):
    """Schema for user preferences response"""
    id: int
    interests: List[str]
    education_level: Optional[str] = None
    field_of_study: Optional[str] = None
    location: Optional[str] = None
    budget_range: Optional[str] = None
    notification_frequency: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
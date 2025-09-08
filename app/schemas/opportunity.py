"""
Opportunity-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.db.models import OpportunityType


class OpportunityBase(BaseModel):
    """Base opportunity schema"""
    title: str
    description: str
    opportunity_type: OpportunityType
    organization: str
    url: Optional[str] = None
    deadline: Optional[datetime] = None
    location: Optional[str] = None
    language: str = "en"
    tags: List[str] = []
    requirements: List[str] = []
    benefits: List[str] = []


class OpportunityCreate(OpportunityBase):
    """Schema for creating an opportunity"""
    pass


class OpportunityUpdate(BaseModel):
    """Schema for updating an opportunity"""
    title: Optional[str] = None
    description: Optional[str] = None
    opportunity_type: Optional[OpportunityType] = None
    organization: Optional[str] = None
    url: Optional[str] = None
    deadline: Optional[datetime] = None
    location: Optional[str] = None
    language: Optional[str] = None
    tags: Optional[List[str]] = None
    requirements: Optional[List[str]] = None
    benefits: Optional[List[str]] = None
    is_active: Optional[bool] = None


class OpportunityResponse(OpportunityBase):
    """Schema for opportunity response"""
    id: int
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SubscriptionCreate(BaseModel):
    """Schema for creating a subscription"""
    opportunity_id: int


class SubscriptionResponse(BaseModel):
    """Schema for subscription response"""
    id: int
    user_id: int
    opportunity_id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class OpportunitySearch(BaseModel):
    """Schema for opportunity search filters"""
    query: Optional[str] = None
    opportunity_type: Optional[OpportunityType] = None
    tags: Optional[List[str]] = None
    location: Optional[str] = None
    language: Optional[str] = None
    limit: int = 20
    offset: int = 0
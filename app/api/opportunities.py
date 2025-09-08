"""
Opportunity management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.schemas.opportunity import (
    OpportunityCreate, OpportunityResponse, OpportunityUpdate,
    SubscriptionCreate, SubscriptionResponse, OpportunitySearch
)
from app.services.opportunity_service import OpportunityService

router = APIRouter()


@router.post("/", response_model=OpportunityResponse)
async def create_opportunity(
    opportunity: OpportunityCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new opportunity"""
    opportunity_service = OpportunityService(db)
    return await opportunity_service.create_opportunity(opportunity)


@router.get("/", response_model=List[OpportunityResponse])
async def get_opportunities(
    search: OpportunitySearch = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Get opportunities with optional search filters"""
    opportunity_service = OpportunityService(db)
    return await opportunity_service.search_opportunities(search)


@router.get("/{opportunity_id}", response_model=OpportunityResponse)
async def get_opportunity(
    opportunity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get opportunity by ID"""
    opportunity_service = OpportunityService(db)
    opportunity = await opportunity_service.get_opportunity(opportunity_id)
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return opportunity


@router.put("/{opportunity_id}", response_model=OpportunityResponse)
async def update_opportunity(
    opportunity_id: int,
    opportunity_update: OpportunityUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update opportunity"""
    opportunity_service = OpportunityService(db)
    opportunity = await opportunity_service.update_opportunity(opportunity_id, opportunity_update)
    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return opportunity


@router.delete("/{opportunity_id}")
async def delete_opportunity(
    opportunity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete opportunity (soft delete)"""
    opportunity_service = OpportunityService(db)
    success = await opportunity_service.delete_opportunity(opportunity_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return {"message": "Opportunity deleted successfully"}


@router.post("/{opportunity_id}/subscribe", response_model=SubscriptionResponse)
async def subscribe_to_opportunity(
    opportunity_id: int,
    user_id: int = Query(..., description="User ID to subscribe"),
    db: AsyncSession = Depends(get_db)
):
    """Subscribe user to an opportunity"""
    opportunity_service = OpportunityService(db)
    subscription = await opportunity_service.subscribe_user(opportunity_id, user_id)
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to create subscription"
        )
    return subscription


@router.delete("/{opportunity_id}/unsubscribe")
async def unsubscribe_from_opportunity(
    opportunity_id: int,
    user_id: int = Query(..., description="User ID to unsubscribe"),
    db: AsyncSession = Depends(get_db)
):
    """Unsubscribe user from an opportunity"""
    opportunity_service = OpportunityService(db)
    success = await opportunity_service.unsubscribe_user(opportunity_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    return {"message": "Unsubscribed successfully"}


@router.get("/user/{user_id}/subscriptions", response_model=List[SubscriptionResponse])
async def get_user_subscriptions(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get user's subscriptions"""
    opportunity_service = OpportunityService(db)
    subscriptions = await opportunity_service.get_user_subscriptions(user_id)
    return subscriptions


@router.get("/user/{user_id}/recommendations", response_model=List[OpportunityResponse])
async def get_user_recommendations(
    user_id: int,
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized opportunity recommendations for user"""
    opportunity_service = OpportunityService(db)
    recommendations = await opportunity_service.get_user_recommendations(user_id, limit)
    return recommendations
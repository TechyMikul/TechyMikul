"""
Dashboard API endpoints for sponsors and mentors
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.core.database import get_db
from app.schemas.opportunity import OpportunityCreate, OpportunityResponse, OpportunityUpdate
from app.services.opportunity_service import OpportunityService
from app.services.user_service import UserService

router = APIRouter()


@router.post("/opportunities", response_model=OpportunityResponse)
async def create_opportunity(
    opportunity: OpportunityCreate,
    creator_id: int = Query(..., description="Creator user ID"),
    db: AsyncSession = Depends(get_db)
):
    """Create a new opportunity (for sponsors/mentors)"""
    opportunity_service = OpportunityService(db)
    return await opportunity_service.create_opportunity(opportunity, creator_id)


@router.get("/opportunities", response_model=List[OpportunityResponse])
async def get_my_opportunities(
    creator_id: int = Query(..., description="Creator user ID"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db)
):
    """Get opportunities created by the user"""
    opportunity_service = OpportunityService(db)
    return await opportunity_service.get_opportunities_by_creator(creator_id)


@router.get("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
async def get_my_opportunity(
    opportunity_id: int,
    creator_id: int = Query(..., description="Creator user ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get specific opportunity created by the user"""
    opportunity_service = OpportunityService(db)
    opportunity = await opportunity_service.get_opportunity(opportunity_id)
    
    if not opportunity or opportunity.created_by != creator_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found or access denied"
        )
    
    return opportunity


@router.put("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
async def update_my_opportunity(
    opportunity_id: int,
    opportunity_update: OpportunityUpdate,
    creator_id: int = Query(..., description="Creator user ID"),
    db: AsyncSession = Depends(get_db)
):
    """Update opportunity created by the user"""
    opportunity_service = OpportunityService(db)
    
    # Check if opportunity exists and belongs to creator
    opportunity = await opportunity_service.get_opportunity(opportunity_id)
    if not opportunity or opportunity.created_by != creator_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found or access denied"
        )
    
    return await opportunity_service.update_opportunity(opportunity_id, opportunity_update)


@router.delete("/opportunities/{opportunity_id}")
async def delete_my_opportunity(
    opportunity_id: int,
    creator_id: int = Query(..., description="Creator user ID"),
    db: AsyncSession = Depends(get_db)
):
    """Delete opportunity created by the user"""
    opportunity_service = OpportunityService(db)
    
    # Check if opportunity exists and belongs to creator
    opportunity = await opportunity_service.get_opportunity(opportunity_id)
    if not opportunity or opportunity.created_by != creator_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found or access denied"
        )
    
    success = await opportunity_service.delete_opportunity(opportunity_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to delete opportunity"
        )
    
    return {"message": "Opportunity deleted successfully"}


@router.get("/opportunities/{opportunity_id}/subscribers")
async def get_opportunity_subscribers(
    opportunity_id: int,
    creator_id: int = Query(..., description="Creator user ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get subscribers for an opportunity (creator only)"""
    opportunity_service = OpportunityService(db)
    
    # Check if opportunity exists and belongs to creator
    opportunity = await opportunity_service.get_opportunity(opportunity_id)
    if not opportunity or opportunity.created_by != creator_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found or access denied"
        )
    
    subscriptions = await opportunity_service.get_opportunity_subscribers(opportunity_id)
    return subscriptions


@router.get("/stats")
async def get_dashboard_stats(
    creator_id: int = Query(..., description="Creator user ID"),
    db: AsyncSession = Depends(get_db)
):
    """Get dashboard statistics for the creator"""
    opportunity_service = OpportunityService(db)
    
    # Get opportunities created by user
    opportunities = await opportunity_service.get_opportunities_by_creator(creator_id)
    
    # Calculate stats
    total_opportunities = len(opportunities)
    active_opportunities = len([opp for opp in opportunities if opp.is_active])
    
    # Get total subscribers across all opportunities
    total_subscribers = 0
    for opportunity in opportunities:
        subscribers = await opportunity_service.get_opportunity_subscribers(opportunity.id)
        total_subscribers += len(subscribers)
    
    # Group by opportunity type
    type_stats = {}
    for opportunity in opportunities:
        opp_type = opportunity.opportunity_type.value
        type_stats[opp_type] = type_stats.get(opp_type, 0) + 1
    
    return {
        "total_opportunities": total_opportunities,
        "active_opportunities": active_opportunities,
        "total_subscribers": total_subscribers,
        "opportunities_by_type": type_stats
    }
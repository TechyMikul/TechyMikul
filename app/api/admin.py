"""
Admin API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.services.admin_service import AdminService

router = APIRouter()


@router.get("/stats")
async def get_platform_stats(db: AsyncSession = Depends(get_db)):
    """Get platform statistics"""
    admin_service = AdminService(db)
    stats = await admin_service.get_platform_stats()
    return stats


@router.get("/users")
async def get_all_users(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get all users (admin only)"""
    admin_service = AdminService(db)
    users = await admin_service.get_all_users(limit, offset)
    return users


@router.get("/opportunities")
async def get_all_opportunities(
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get all opportunities (admin only)"""
    admin_service = AdminService(db)
    opportunities = await admin_service.get_all_opportunities(limit, offset)
    return opportunities


@router.post("/opportunities/{opportunity_id}/approve")
async def approve_opportunity(
    opportunity_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Approve an opportunity"""
    admin_service = AdminService(db)
    success = await admin_service.approve_opportunity(opportunity_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return {"message": "Opportunity approved successfully"}


@router.post("/opportunities/{opportunity_id}/reject")
async def reject_opportunity(
    opportunity_id: int,
    reason: str,
    db: AsyncSession = Depends(get_db)
):
    """Reject an opportunity"""
    admin_service = AdminService(db)
    success = await admin_service.reject_opportunity(opportunity_id, reason)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )
    return {"message": "Opportunity rejected successfully"}
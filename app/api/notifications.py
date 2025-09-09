"""
Notification management API endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.core.database import get_db
from app.services.notification_service import NotificationService

router = APIRouter()


@router.get("/user/{user_id}")
async def get_user_notifications(
    user_id: int,
    limit: int = 20,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """Get user's notifications"""
    notification_service = NotificationService(db)
    notifications = await notification_service.get_user_notifications(user_id, limit, offset)
    return notifications


@router.post("/user/{user_id}/mark-read")
async def mark_notifications_read(
    user_id: int,
    notification_ids: List[int],
    db: AsyncSession = Depends(get_db)
):
    """Mark notifications as read"""
    notification_service = NotificationService(db)
    success = await notification_service.mark_notifications_read(user_id, notification_ids)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to mark notifications as read"
        )
    return {"message": "Notifications marked as read"}


@router.post("/send-opportunity-alert")
async def send_opportunity_alert(
    opportunity_id: int,
    user_ids: List[int] = None,
    db: AsyncSession = Depends(get_db)
):
    """Send opportunity alert to users"""
    notification_service = NotificationService(db)
    success = await notification_service.send_opportunity_alert(opportunity_id, user_ids)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to send opportunity alert"
        )
    return {"message": "Opportunity alert sent successfully"}
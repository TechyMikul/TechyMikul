"""
Admin service for platform management
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from typing import Dict, Any, List
from app.db.models import User, Opportunity, Subscription, Notification, UserType, OpportunityType


class AdminService:
    """Admin service for platform management"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_platform_stats(self) -> Dict[str, Any]:
        """Get platform statistics"""
        # User statistics
        total_users_result = await self.db.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar()
        
        active_users_result = await self.db.execute(
            select(func.count(User.id)).where(User.is_active == True)
        )
        active_users = active_users_result.scalar()
        
        # User type breakdown
        user_type_stats = {}
        for user_type in UserType:
            result = await self.db.execute(
                select(func.count(User.id)).where(
                    and_(User.user_type == user_type, User.is_active == True)
                )
            )
            user_type_stats[user_type.value] = result.scalar()
        
        # Opportunity statistics
        total_opportunities_result = await self.db.execute(select(func.count(Opportunity.id)))
        total_opportunities = total_opportunities_result.scalar()
        
        active_opportunities_result = await self.db.execute(
            select(func.count(Opportunity.id)).where(Opportunity.is_active == True)
        )
        active_opportunities = active_opportunities_result.scalar()
        
        # Opportunity type breakdown
        opportunity_type_stats = {}
        for opp_type in OpportunityType:
            result = await self.db.execute(
                select(func.count(Opportunity.id)).where(
                    and_(Opportunity.opportunity_type == opp_type, Opportunity.is_active == True)
                )
            )
            opportunity_type_stats[opp_type.value] = result.scalar()
        
        # Subscription statistics
        total_subscriptions_result = await self.db.execute(
            select(func.count(Subscription.id)).where(Subscription.is_active == True)
        )
        total_subscriptions = total_subscriptions_result.scalar()
        
        # Notification statistics
        total_notifications_result = await self.db.execute(select(func.count(Notification.id)))
        total_notifications = total_notifications_result.scalar()
        
        return {
            "users": {
                "total": total_users,
                "active": active_users,
                "by_type": user_type_stats
            },
            "opportunities": {
                "total": total_opportunities,
                "active": active_opportunities,
                "by_type": opportunity_type_stats
            },
            "subscriptions": {
                "total": total_subscriptions
            },
            "notifications": {
                "total": total_notifications
            }
        }
    
    async def get_all_users(self, limit: int = 50, offset: int = 0) -> List[User]:
        """Get all users with pagination"""
        result = await self.db.execute(
            select(User)
            .options(selectinload(User.platforms), selectinload(User.preferences))
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all_opportunities(self, limit: int = 50, offset: int = 0) -> List[Opportunity]:
        """Get all opportunities with pagination"""
        result = await self.db.execute(
            select(Opportunity)
            .options(selectinload(Opportunity.creator))
            .order_by(Opportunity.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def approve_opportunity(self, opportunity_id: int) -> bool:
        """Approve an opportunity"""
        result = await self.db.execute(
            select(Opportunity).where(Opportunity.id == opportunity_id)
        )
        opportunity = result.scalar_one_or_none()
        
        if not opportunity:
            return False
        
        # In a real implementation, you might have an approval status field
        # For now, we'll just ensure it's active
        opportunity.is_active = True
        await self.db.commit()
        return True
    
    async def reject_opportunity(self, opportunity_id: int, reason: str) -> bool:
        """Reject an opportunity"""
        result = await self.db.execute(
            select(Opportunity).where(Opportunity.id == opportunity_id)
        )
        opportunity = result.scalar_one_or_none()
        
        if not opportunity:
            return False
        
        # Deactivate the opportunity
        opportunity.is_active = False
        await self.db.commit()
        return True
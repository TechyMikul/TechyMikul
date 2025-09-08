"""
Opportunity service for business logic
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.orm import selectinload
from typing import Optional, List
from app.db.models import Opportunity, Subscription, User, UserPreferences
from app.schemas.opportunity import OpportunityCreate, OpportunityUpdate, OpportunitySearch


class OpportunityService:
    """Opportunity service for handling opportunity-related operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_opportunity(self, opportunity_data: OpportunityCreate, created_by: int) -> Opportunity:
        """Create a new opportunity"""
        opportunity = Opportunity(
            **opportunity_data.model_dump(),
            created_by=created_by
        )
        self.db.add(opportunity)
        await self.db.commit()
        await self.db.refresh(opportunity)
        return opportunity
    
    async def get_opportunity(self, opportunity_id: int) -> Optional[Opportunity]:
        """Get opportunity by ID"""
        result = await self.db.execute(
            select(Opportunity)
            .options(selectinload(Opportunity.creator))
            .where(Opportunity.id == opportunity_id)
        )
        return result.scalar_one_or_none()
    
    async def search_opportunities(self, search: OpportunitySearch) -> List[Opportunity]:
        """Search opportunities with filters"""
        query = select(Opportunity).where(Opportunity.is_active == True)
        
        if search.query:
            query = query.where(
                or_(
                    Opportunity.title.ilike(f"%{search.query}%"),
                    Opportunity.description.ilike(f"%{search.query}%"),
                    Opportunity.organization.ilike(f"%{search.query}%")
                )
            )
        
        if search.opportunity_type:
            query = query.where(Opportunity.opportunity_type == search.opportunity_type)
        
        if search.tags:
            # Search for opportunities that contain any of the specified tags
            tag_conditions = [Opportunity.tags.contains([tag]) for tag in search.tags]
            query = query.where(or_(*tag_conditions))
        
        if search.location:
            query = query.where(Opportunity.location.ilike(f"%{search.location}%"))
        
        if search.language:
            query = query.where(Opportunity.language == search.language)
        
        query = query.offset(search.offset).limit(search.limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_opportunity(self, opportunity_id: int, opportunity_update: OpportunityUpdate) -> Optional[Opportunity]:
        """Update opportunity"""
        update_data = opportunity_update.model_dump(exclude_unset=True)
        if not update_data:
            return await self.get_opportunity(opportunity_id)
        
        await self.db.execute(
            update(Opportunity)
            .where(Opportunity.id == opportunity_id)
            .values(**update_data)
        )
        await self.db.commit()
        return await self.get_opportunity(opportunity_id)
    
    async def delete_opportunity(self, opportunity_id: int) -> bool:
        """Soft delete opportunity"""
        result = await self.db.execute(
            update(Opportunity)
            .where(Opportunity.id == opportunity_id)
            .values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def subscribe_user(self, opportunity_id: int, user_id: int) -> Optional[Subscription]:
        """Subscribe user to an opportunity"""
        # Check if subscription already exists
        existing = await self.db.execute(
            select(Subscription).where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.opportunity_id == opportunity_id
                )
            )
        )
        if existing.scalar_one_or_none():
            return None  # Already subscribed
        
        subscription = Subscription(
            user_id=user_id,
            opportunity_id=opportunity_id
        )
        self.db.add(subscription)
        await self.db.commit()
        await self.db.refresh(subscription)
        return subscription
    
    async def unsubscribe_user(self, opportunity_id: int, user_id: int) -> bool:
        """Unsubscribe user from an opportunity"""
        result = await self.db.execute(
            update(Subscription)
            .where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.opportunity_id == opportunity_id
                )
            )
            .values(is_active=False)
        )
        await self.db.commit()
        return result.rowcount > 0
    
    async def get_user_subscriptions(self, user_id: int) -> List[Subscription]:
        """Get user's subscriptions"""
        result = await self.db.execute(
            select(Subscription)
            .options(selectinload(Subscription.opportunity))
            .where(
                and_(
                    Subscription.user_id == user_id,
                    Subscription.is_active == True
                )
            )
        )
        return result.scalars().all()
    
    async def get_user_recommendations(self, user_id: int, limit: int = 10) -> List[Opportunity]:
        """Get personalized opportunity recommendations for user"""
        # Get user preferences
        user_prefs_result = await self.db.execute(
            select(UserPreferences).where(UserPreferences.user_id == user_id)
        )
        user_prefs = user_prefs_result.scalar_one_or_none()
        
        if not user_prefs:
            # If no preferences, return recent opportunities
            result = await self.db.execute(
                select(Opportunity)
                .where(Opportunity.is_active == True)
                .order_by(Opportunity.created_at.desc())
                .limit(limit)
            )
            return result.scalars().all()
        
        # Build recommendation query based on preferences
        query = select(Opportunity).where(Opportunity.is_active == True)
        
        # Filter by interests (tags)
        if user_prefs.interests:
            tag_conditions = [Opportunity.tags.contains([interest]) for interest in user_prefs.interests]
            query = query.where(or_(*tag_conditions))
        
        # Filter by field of study
        if user_prefs.field_of_study:
            query = query.where(
                or_(
                    Opportunity.title.ilike(f"%{user_prefs.field_of_study}%"),
                    Opportunity.description.ilike(f"%{user_prefs.field_of_study}%")
                )
            )
        
        # Filter by location
        if user_prefs.location:
            query = query.where(Opportunity.location.ilike(f"%{user_prefs.location}%"))
        
        # Order by relevance and recency
        query = query.order_by(Opportunity.created_at.desc()).limit(limit)
        
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_opportunities_by_creator(self, creator_id: int) -> List[Opportunity]:
        """Get opportunities created by a specific user"""
        result = await self.db.execute(
            select(Opportunity)
            .where(Opportunity.created_by == creator_id)
            .order_by(Opportunity.created_at.desc())
        )
        return result.scalars().all()
    
    async def get_opportunity_subscribers(self, opportunity_id: int) -> List[Subscription]:
        """Get subscribers for a specific opportunity"""
        result = await self.db.execute(
            select(Subscription)
            .options(selectinload(Subscription.user))
            .where(
                and_(
                    Subscription.opportunity_id == opportunity_id,
                    Subscription.is_active == True
                )
            )
        )
        return result.scalars().all()
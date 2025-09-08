"""
Notification service for handling notifications
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_
from typing import List, Optional
from app.db.models import Notification, User, UserPlatform, Opportunity
from app.bots.telegram_bot import TelegramBot
from app.bots.discord_bot import DiscordBot
from app.bots.whatsapp_bot import WhatsAppBot


class NotificationService:
    """Notification service for handling notifications"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.telegram_bot = TelegramBot()
        self.discord_bot = DiscordBot()
        self.whatsapp_bot = WhatsAppBot()
    
    async def get_user_notifications(self, user_id: int, limit: int = 20, offset: int = 0) -> List[Notification]:
        """Get user's notifications"""
        result = await self.db.execute(
            select(Notification)
            .where(Notification.user_id == user_id)
            .order_by(Notification.sent_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def mark_notifications_read(self, user_id: int, notification_ids: List[int]) -> bool:
        """Mark notifications as read"""
        await self.db.execute(
            update(Notification)
            .where(
                and_(
                    Notification.user_id == user_id,
                    Notification.id.in_(notification_ids)
                )
            )
            .values(is_read=True)
        )
        await self.db.commit()
        return True
    
    async def send_opportunity_alert(self, opportunity_id: int, user_ids: Optional[List[int]] = None) -> bool:
        """Send opportunity alert to users"""
        # Get opportunity
        opportunity_result = await self.db.execute(
            select(Opportunity).where(Opportunity.id == opportunity_id)
        )
        opportunity = opportunity_result.scalar_one_or_none()
        
        if not opportunity:
            return False
        
        # Get target users
        if user_ids:
            # Send to specific users
            users_result = await self.db.execute(
                select(User)
                .options(selectinload(User.platforms))
                .where(User.id.in_(user_ids))
            )
            users = users_result.scalars().all()
        else:
            # Send to all subscribed users
            users_result = await self.db.execute(
                select(User)
                .options(selectinload(User.platforms))
                .join(Subscription)
                .where(Subscription.opportunity_id == opportunity_id)
            )
            users = users_result.scalars().all()
        
        # Send notifications to each user's platforms
        for user in users:
            await self._send_to_user_platforms(user, opportunity)
        
        return True
    
    async def _send_to_user_platforms(self, user: User, opportunity: Opportunity) -> None:
        """Send notification to all user's active platforms"""
        for platform in user.platforms:
            if not platform.is_active:
                continue
            
            message = self._format_opportunity_message(opportunity)
            
            try:
                if platform.platform.value == "telegram":
                    await self.telegram_bot.send_message(platform.platform_user_id, message)
                elif platform.platform.value == "discord":
                    await self.discord_bot.send_message(platform.platform_user_id, message)
                elif platform.platform.value == "whatsapp":
                    await self.whatsapp_bot.send_message(platform.platform_user_id, message)
                
                # Record notification in database
                await self._record_notification(user.id, opportunity.id, platform.platform.value, message)
                
            except Exception as e:
                print(f"Failed to send notification to {platform.platform.value} user {platform.platform_user_id}: {e}")
    
    def _format_opportunity_message(self, opportunity: Opportunity) -> str:
        """Format opportunity data into a user-friendly message"""
        message = f"🎓 *{opportunity.title}*\n\n"
        message += f"📝 {opportunity.description[:200]}...\n\n"
        message += f"🏢 Organization: {opportunity.organization}\n"
        
        if opportunity.deadline:
            message += f"⏰ Deadline: {opportunity.deadline.strftime('%Y-%m-%d')}\n"
        
        if opportunity.location:
            message += f"📍 Location: {opportunity.location}\n"
        
        if opportunity.url:
            message += f"🔗 Learn more: {opportunity.url}\n"
        
        if opportunity.tags:
            tags = ", ".join(opportunity.tags[:5])  # Limit to 5 tags
            message += f"🏷️ Tags: {tags}\n"
        
        return message
    
    async def _record_notification(self, user_id: int, opportunity_id: int, platform: str, message: str) -> None:
        """Record notification in database"""
        notification = Notification(
            user_id=user_id,
            opportunity_id=opportunity_id,
            platform=platform,
            message=message
        )
        self.db.add(notification)
        await self.db.commit()
    
    async def send_welcome_message(self, user: User) -> None:
        """Send welcome message to new user"""
        welcome_message = f"""
🎓 *Welcome to EduOpportunity Bot!*

Hello {user.first_name}! I'm here to help you discover amazing educational opportunities.

Use /help to see available commands and /preferences to set your preferences for personalized recommendations.
        """
        
        for platform in user.platforms:
            if not platform.is_active:
                continue
            
            try:
                if platform.platform.value == "telegram":
                    await self.telegram_bot.send_message(platform.platform_user_id, welcome_message)
                elif platform.platform.value == "discord":
                    await self.discord_bot.send_message(platform.platform_user_id, welcome_message)
                elif platform.platform.value == "whatsapp":
                    await self.whatsapp_bot.send_message(platform.platform_user_id, welcome_message)
            except Exception as e:
                print(f"Failed to send welcome message to {platform.platform.value} user {platform.platform_user_id}: {e}")
"""
Base bot class for all platform implementations
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from app.db.models import Platform, UserType
from app.schemas.user import UserCreate, UserPreferencesCreate


class BaseBot(ABC):
    """Base class for all bot implementations"""
    
    def __init__(self, platform: Platform):
        self.platform = platform
    
    @abstractmethod
    async def start(self) -> None:
        """Start the bot"""
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        """Stop the bot"""
        pass
    
    @abstractmethod
    async def send_message(self, user_id: str, message: str, **kwargs) -> bool:
        """Send a message to a user"""
        pass
    
    @abstractmethod
    async def handle_message(self, message_data: Dict[str, Any]) -> None:
        """Handle incoming message"""
        pass
    
    async def register_user(self, platform_user_id: str, user_data: Dict[str, Any]) -> Optional[int]:
        """Register a new user from bot interaction"""
        # This will be implemented in the service layer
        pass
    
    async def get_user_preferences(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user preferences for personalization"""
        # This will be implemented in the service layer
        pass
    
    async def send_opportunity_alert(self, user_id: str, opportunity: Dict[str, Any]) -> bool:
        """Send opportunity alert to user"""
        message = self._format_opportunity_message(opportunity)
        return await self.send_message(user_id, message)
    
    def _format_opportunity_message(self, opportunity: Dict[str, Any]) -> str:
        """Format opportunity data into a user-friendly message"""
        message = f"🎓 *{opportunity['title']}*\n\n"
        message += f"📝 {opportunity['description'][:200]}...\n\n"
        message += f"🏢 Organization: {opportunity['organization']}\n"
        
        if opportunity.get('deadline'):
            message += f"⏰ Deadline: {opportunity['deadline']}\n"
        
        if opportunity.get('location'):
            message += f"📍 Location: {opportunity['location']}\n"
        
        if opportunity.get('url'):
            message += f"🔗 Learn more: {opportunity['url']}\n"
        
        if opportunity.get('tags'):
            tags = ", ".join(opportunity['tags'][:5])  # Limit to 5 tags
            message += f"🏷️ Tags: {tags}\n"
        
        return message
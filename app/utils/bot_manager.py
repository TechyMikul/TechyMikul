"""
Bot manager for coordinating multiple platform bots
"""
import asyncio
import logging
from typing import Dict, List, Optional
from app.bots.telegram_bot import TelegramBot
from app.bots.discord_bot import DiscordBot
from app.bots.whatsapp_bot import WhatsAppBot
from app.core.config import settings

logger = logging.getLogger(__name__)


class BotManager:
    """Manager for coordinating all platform bots"""
    
    def __init__(self):
        self.bots: Dict[str, any] = {}
        self.tasks: List[asyncio.Task] = []
    
    async def start_all_bots(self) -> None:
        """Start all configured bots"""
        # Start Telegram bot
        if settings.TELEGRAM_BOT_TOKEN:
            telegram_bot = TelegramBot()
            self.bots['telegram'] = telegram_bot
            task = asyncio.create_task(telegram_bot.start())
            self.tasks.append(task)
            logger.info("Telegram bot started")
        
        # Start Discord bot
        if settings.DISCORD_BOT_TOKEN:
            discord_bot = DiscordBot()
            self.bots['discord'] = discord_bot
            task = asyncio.create_task(discord_bot.start())
            self.tasks.append(task)
            logger.info("Discord bot started")
        
        # Start WhatsApp bot
        if all([settings.WHATSAPP_ACCOUNT_SID, settings.WHATSAPP_AUTH_TOKEN, settings.WHATSAPP_PHONE_NUMBER]):
            whatsapp_bot = WhatsAppBot()
            self.bots['whatsapp'] = whatsapp_bot
            await whatsapp_bot.start()
            logger.info("WhatsApp bot started")
    
    async def stop_all_bots(self) -> None:
        """Stop all running bots"""
        # Cancel all tasks
        for task in self.tasks:
            task.cancel()
        
        # Wait for tasks to complete
        if self.tasks:
            await asyncio.gather(*self.tasks, return_exceptions=True)
        
        # Stop individual bots
        for bot in self.bots.values():
            await bot.stop()
        
        logger.info("All bots stopped")
    
    async def send_message_to_user(self, user_id: str, platform: str, message: str, **kwargs) -> bool:
        """Send message to user on specific platform"""
        if platform not in self.bots:
            logger.error(f"Bot for platform {platform} not available")
            return False
        
        bot = self.bots[platform]
        return await bot.send_message(user_id, message, **kwargs)
    
    async def send_message_to_all_platforms(self, user_platforms: List[Dict], message: str, **kwargs) -> Dict[str, bool]:
        """Send message to user across all their platforms"""
        results = {}
        
        for platform_info in user_platforms:
            platform = platform_info['platform']
            platform_user_id = platform_info['platform_user_id']
            
            success = await self.send_message_to_user(platform_user_id, platform, message, **kwargs)
            results[platform] = success
        
        return results
    
    def get_bot(self, platform: str):
        """Get bot instance for specific platform"""
        return self.bots.get(platform)
    
    async def handle_webhook(self, platform: str, webhook_data: Dict) -> Optional[str]:
        """Handle webhook data for specific platform"""
        if platform not in self.bots:
            logger.error(f"Bot for platform {platform} not available")
            return None
        
        bot = self.bots[platform]
        return await bot.handle_message(webhook_data)


# Global bot manager instance
bot_manager = BotManager()
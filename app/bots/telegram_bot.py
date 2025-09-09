"""
Telegram bot implementation
"""
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from typing import Dict, Any
from app.bots.base import BaseBot
from app.db.models import Platform
from app.core.config import settings

logger = logging.getLogger(__name__)


class TelegramBot(BaseBot):
    """Telegram bot implementation"""
    
    def __init__(self):
        super().__init__(Platform.TELEGRAM)
        self.application = None
        self.bot = None
    
    async def start(self) -> None:
        """Start the Telegram bot"""
        if not settings.TELEGRAM_BOT_TOKEN:
            logger.warning("Telegram bot token not configured")
            return
        
        self.application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self._handle_start))
        self.application.add_handler(CommandHandler("help", self._handle_help))
        self.application.add_handler(CommandHandler("register", self._handle_register))
        self.application.add_handler(CommandHandler("preferences", self._handle_preferences))
        self.application.add_handler(CommandHandler("opportunities", self._handle_opportunities))
        self.application.add_handler(CommandHandler("subscribe", self._handle_subscribe))
        self.application.add_handler(CommandHandler("unsubscribe", self._handle_unsubscribe))
        self.application.add_handler(CallbackQueryHandler(self._handle_callback))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_text))
        
        # Start the bot
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        logger.info("Telegram bot started")
    
    async def stop(self) -> None:
        """Stop the Telegram bot"""
        if self.application:
            await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()
            logger.info("Telegram bot stopped")
    
    async def send_message(self, user_id: str, message: str, **kwargs) -> bool:
        """Send a message to a user"""
        try:
            if self.application and self.application.bot:
                await self.application.bot.send_message(
                    chat_id=user_id,
                    text=message,
                    parse_mode='Markdown',
                    **kwargs
                )
                return True
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")
        return False
    
    async def handle_message(self, message_data: Dict[str, Any]) -> None:
        """Handle incoming message (for webhook mode)"""
        # This would be used if running in webhook mode
        pass
    
    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /start command"""
        user = update.effective_user
        welcome_message = f"""
🎓 *Welcome to EduOpportunity Bot!*

Hello {user.first_name}! I'm here to help you discover amazing educational opportunities including:
• 🎓 Scholarships
• 📚 Free learning resources  
• 🎪 Events and workshops
• 👥 Mentorship programs
• 💰 Funding opportunities

Use /register to get started and /help to see all available commands.
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Register", callback_data="register")],
            [InlineKeyboardButton("❓ Help", callback_data="help")],
            [InlineKeyboardButton("🔍 Browse Opportunities", callback_data="opportunities")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /help command"""
        help_message = """
🤖 *Available Commands:*

/start - Welcome message and main menu
/register - Register as a student
/preferences - Set your preferences
/opportunities - Browse available opportunities
/subscribe <id> - Subscribe to an opportunity
/unsubscribe <id> - Unsubscribe from an opportunity
/help - Show this help message

💡 *Tips:*
• Set your preferences to get personalized recommendations
• Use the inline buttons for easy navigation
• Contact support if you need help
        """
        await update.message.reply_text(help_message, parse_mode='Markdown')
    
    async def _handle_register(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /register command"""
        user = update.effective_user
        
        # Check if user is already registered
        # This would integrate with the user service
        
        registration_message = f"""
📝 *Registration*

Hi {user.first_name}! Let's get you registered.

Please provide the following information:
1. Your email address
2. Your field of study
3. Your education level
4. Your interests (comma-separated)

Example:
Email: john@example.com
Field: Computer Science
Level: Undergraduate
Interests: AI, Machine Learning, Web Development
        """
        
        await update.message.reply_text(registration_message, parse_mode='Markdown')
    
    async def _handle_preferences(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /preferences command"""
        preferences_message = """
⚙️ *Preferences Settings*

Set your preferences to get personalized opportunity recommendations:

1. **Interests**: What topics interest you?
2. **Education Level**: High School, Undergraduate, Graduate, etc.
3. **Field of Study**: Your major or area of focus
4. **Location**: Your preferred location
5. **Notification Frequency**: How often to receive alerts

Use the format:
/preferences interests:AI,ML field:Computer Science level:Undergraduate
        """
        await update.message.reply_text(preferences_message, parse_mode='Markdown')
    
    async def _handle_opportunities(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /opportunities command"""
        # This would fetch opportunities from the database
        opportunities_message = """
🔍 *Available Opportunities*

Here are some opportunities that match your preferences:

1. **AI Research Scholarship** - $5000
   Deadline: 2024-03-15
   [Subscribe] [Learn More]

2. **Free Python Course** - Online
   Duration: 8 weeks
   [Subscribe] [Learn More]

3. **Tech Conference 2024** - San Francisco
   Date: 2024-04-20
   [Subscribe] [Learn More]

Use /subscribe <number> to subscribe to an opportunity.
        """
        await update.message.reply_text(opportunities_message, parse_mode='Markdown')
    
    async def _handle_subscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /subscribe command"""
        if not context.args:
            await update.message.reply_text("Please provide an opportunity ID. Example: /subscribe 1")
            return
        
        try:
            opportunity_id = int(context.args[0])
            # This would integrate with the subscription service
            await update.message.reply_text(f"✅ Subscribed to opportunity {opportunity_id}")
        except ValueError:
            await update.message.reply_text("Please provide a valid opportunity ID (number)")
    
    async def _handle_unsubscribe(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle /unsubscribe command"""
        if not context.args:
            await update.message.reply_text("Please provide an opportunity ID. Example: /unsubscribe 1")
            return
        
        try:
            opportunity_id = int(context.args[0])
            # This would integrate with the subscription service
            await update.message.reply_text(f"❌ Unsubscribed from opportunity {opportunity_id}")
        except ValueError:
            await update.message.reply_text("Please provide a valid opportunity ID (number)")
    
    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle callback queries from inline keyboards"""
        query = update.callback_query
        await query.answer()
        
        if query.data == "register":
            await self._handle_register(update, context)
        elif query.data == "help":
            await self._handle_help(update, context)
        elif query.data == "opportunities":
            await self._handle_opportunities(update, context)
    
    async def _handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Handle text messages"""
        # This would process natural language and provide appropriate responses
        await update.message.reply_text(
            "I'm here to help you find educational opportunities! Use /help to see available commands."
        )
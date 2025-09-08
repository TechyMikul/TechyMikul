"""
WhatsApp bot implementation using Twilio
"""
import logging
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from typing import Dict, Any
from app.bots.base import BaseBot
from app.db.models import Platform
from app.core.config import settings

logger = logging.getLogger(__name__)


class WhatsAppBot(BaseBot):
    """WhatsApp bot implementation using Twilio"""
    
    def __init__(self):
        super().__init__(Platform.WHATSAPP)
        self.client = None
        self.phone_number = None
    
    async def start(self) -> None:
        """Start the WhatsApp bot"""
        if not all([settings.WHATSAPP_ACCOUNT_SID, settings.WHATSAPP_AUTH_TOKEN, settings.WHATSAPP_PHONE_NUMBER]):
            logger.warning("WhatsApp bot credentials not configured")
            return
        
        self.client = Client(settings.WHATSAPP_ACCOUNT_SID, settings.WHATSAPP_AUTH_TOKEN)
        self.phone_number = settings.WHATSAPP_PHONE_NUMBER
        
        logger.info("WhatsApp bot initialized")
    
    async def stop(self) -> None:
        """Stop the WhatsApp bot"""
        logger.info("WhatsApp bot stopped")
    
    async def send_message(self, user_id: str, message: str, **kwargs) -> bool:
        """Send a message to a user"""
        try:
            if self.client:
                message_obj = self.client.messages.create(
                    body=message,
                    from_=f"whatsapp:{self.phone_number}",
                    to=f"whatsapp:{user_id}"
                )
                logger.info(f"Message sent to {user_id}: {message_obj.sid}")
                return True
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")
        return False
    
    async def handle_message(self, message_data: Dict[str, Any]) -> None:
        """Handle incoming message from webhook"""
        try:
            from_number = message_data.get('From', '').replace('whatsapp:', '')
            message_body = message_data.get('Body', '')
            
            logger.info(f"Received message from {from_number}: {message_body}")
            
            # Process the message and generate response
            response = await self._process_message(from_number, message_body)
            
            # Return TwiML response
            return self._create_twiml_response(response)
            
        except Exception as e:
            logger.error(f"Error handling WhatsApp message: {e}")
            return self._create_twiml_response("Sorry, I encountered an error. Please try again later.")
    
    def _create_twiml_response(self, message: str) -> str:
        """Create TwiML response for WhatsApp"""
        response = MessagingResponse()
        response.message(message)
        return str(response)
    
    async def _process_message(self, from_number: str, message: str) -> str:
        """Process incoming message and generate response"""
        message_lower = message.lower().strip()
        
        if message_lower in ['/start', 'start', 'hi', 'hello']:
            return await self._handle_start(from_number)
        elif message_lower in ['/help', 'help']:
            return await self._handle_help()
        elif message_lower in ['/register', 'register']:
            return await self._handle_register()
        elif message_lower in ['/preferences', 'preferences']:
            return await self._handle_preferences()
        elif message_lower in ['/opportunities', 'opportunities']:
            return await self._handle_opportunities()
        else:
            return await self._handle_general_message(message)
    
    async def _handle_start(self, from_number: str) -> str:
        """Handle start command"""
        return f"""
🎓 *Welcome to EduOpportunity Bot!*

I'm here to help you discover amazing educational opportunities including:
• 🎓 Scholarships
• 📚 Free learning resources  
• 🎪 Events and workshops
• 👥 Mentorship programs
• 💰 Funding opportunities

*Available Commands:*
/register - Get started
/preferences - Set your preferences
/opportunities - Browse opportunities
/help - See all commands

Reply with any command to get started!
        """
    
    async def _handle_help(self) -> str:
        """Handle help command"""
        return """
🤖 *Available Commands:*

/start - Welcome message
/register - Register as a student
/preferences - Set your preferences
/opportunities - Browse available opportunities
/subscribe <id> - Subscribe to an opportunity
/unsubscribe <id> - Unsubscribe from an opportunity
/help - Show this help message

💡 *Tips:*
• Set your preferences to get personalized recommendations
• Use the bot for private conversations
• Contact support if you need help
        """
    
    async def _handle_register(self) -> str:
        """Handle register command"""
        return """
📝 *Registration*

Let's get you registered! Please provide the following information:

1. *Email address*
2. *Field of study*
3. *Education level*
4. *Interests* (comma-separated)

*Example:*
Email: john@example.com
Field: Computer Science
Level: Undergraduate
Interests: AI, Machine Learning, Web Development

Reply with your information in this format.
        """
    
    async def _handle_preferences(self) -> str:
        """Handle preferences command"""
        return """
⚙️ *Preferences Settings*

Set your preferences to get personalized opportunity recommendations:

1. *Interests*: What topics interest you?
2. *Education Level*: High School, Undergraduate, Graduate, etc.
3. *Field of Study*: Your major or area of focus
4. *Location*: Your preferred location
5. *Notification Frequency*: How often to receive alerts

*Format:*
interests: AI,ML
field: Computer Science
level: Undergraduate
location: San Francisco
frequency: daily

Reply with your preferences in this format.
        """
    
    async def _handle_opportunities(self) -> str:
        """Handle opportunities command"""
        return """
🔍 *Available Opportunities*

Here are some opportunities that match your preferences:

1. *AI Research Scholarship* - $5000
   Deadline: 2024-03-15
   Reply: SUBSCRIBE 1

2. *Free Python Course* - Online
   Duration: 8 weeks
   Reply: SUBSCRIBE 2

3. *Tech Conference 2024* - San Francisco
   Date: 2024-04-20
   Reply: SUBSCRIBE 3

Reply with SUBSCRIBE <number> to subscribe to an opportunity.
        """
    
    async def _handle_general_message(self, message: str) -> str:
        """Handle general messages"""
        return """
I'm here to help you find educational opportunities! 

Use /help to see available commands or /start to begin.

What would you like to do?
        """
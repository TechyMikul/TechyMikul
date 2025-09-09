"""
Discord bot implementation
"""
import logging
import discord
from discord.ext import commands
from typing import Dict, Any
from app.bots.base import BaseBot
from app.db.models import Platform
from app.core.config import settings

logger = logging.getLogger(__name__)


class DiscordBot(BaseBot):
    """Discord bot implementation"""
    
    def __init__(self):
        super().__init__(Platform.DISCORD)
        self.bot = None
    
    async def start(self) -> None:
        """Start the Discord bot"""
        if not settings.DISCORD_BOT_TOKEN:
            logger.warning("Discord bot token not configured")
            return
        
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        # Add event handlers
        self.bot.add_listener(self._on_ready)
        self.bot.add_listener(self._on_message)
        
        # Add command handlers
        self.bot.add_command(commands.Command('start', self._handle_start))
        self.bot.add_command(commands.Command('help', self._handle_help))
        self.bot.add_command(commands.Command('register', self._handle_register))
        self.bot.add_command(commands.Command('preferences', self._handle_preferences))
        self.bot.add_command(commands.Command('opportunities', self._handle_opportunities))
        self.bot.add_command(commands.Command('subscribe', self._handle_subscribe))
        self.bot.add_command(commands.Command('unsubscribe', self._handle_unsubscribe))
        
        # Start the bot
        await self.bot.start(settings.DISCORD_BOT_TOKEN)
    
    async def stop(self) -> None:
        """Stop the Discord bot"""
        if self.bot:
            await self.bot.close()
            logger.info("Discord bot stopped")
    
    async def send_message(self, user_id: str, message: str, **kwargs) -> bool:
        """Send a message to a user"""
        try:
            if self.bot:
                user = await self.bot.fetch_user(int(user_id))
                await user.send(message, **kwargs)
                return True
        except Exception as e:
            logger.error(f"Failed to send message to {user_id}: {e}")
        return False
    
    async def handle_message(self, message_data: Dict[str, Any]) -> None:
        """Handle incoming message"""
        # This would be used for webhook mode
        pass
    
    async def _on_ready(self) -> None:
        """Event handler for when bot is ready"""
        logger.info(f"Discord bot logged in as {self.bot.user}")
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="for educational opportunities"
            )
        )
    
    async def _on_message(self, message) -> None:
        """Event handler for messages"""
        if message.author == self.bot.user:
            return
        
        # Process commands
        await self.bot.process_commands(message)
    
    async def _handle_start(self, ctx) -> None:
        """Handle !start command"""
        welcome_message = f"""
🎓 **Welcome to EduOpportunity Bot!**

Hello {ctx.author.display_name}! I'm here to help you discover amazing educational opportunities including:
• 🎓 Scholarships
• 📚 Free learning resources  
• 🎪 Events and workshops
• 👥 Mentorship programs
• 💰 Funding opportunities

Use `!register` to get started and `!help` to see all available commands.
        """
        
        embed = discord.Embed(
            title="🎓 EduOpportunity Bot",
            description=welcome_message,
            color=0x00ff00
        )
        embed.add_field(
            name="Quick Actions",
            value="`!register` - Get started\n`!help` - See commands\n`!opportunities` - Browse opportunities",
            inline=False
        )
        
        await ctx.send(embed=embed)
    
    async def _handle_help(self, ctx) -> None:
        """Handle !help command"""
        help_message = """
🤖 **Available Commands:**

`!start` - Welcome message and main menu
`!register` - Register as a student
`!preferences` - Set your preferences
`!opportunities` - Browse available opportunities
`!subscribe <id>` - Subscribe to an opportunity
`!unsubscribe <id>` - Unsubscribe from an opportunity
`!help` - Show this help message

💡 **Tips:**
• Set your preferences to get personalized recommendations
• Use the bot in DMs for private interactions
• Contact support if you need help
        """
        
        embed = discord.Embed(
            title="🤖 Help & Commands",
            description=help_message,
            color=0x0099ff
        )
        
        await ctx.send(embed=embed)
    
    async def _handle_register(self, ctx) -> None:
        """Handle !register command"""
        registration_message = f"""
📝 **Registration**

Hi {ctx.author.display_name}! Let's get you registered.

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
        
        embed = discord.Embed(
            title="📝 Registration",
            description=registration_message,
            color=0xff9900
        )
        
        await ctx.send(embed=embed)
    
    async def _handle_preferences(self, ctx) -> None:
        """Handle !preferences command"""
        preferences_message = """
⚙️ **Preferences Settings**

Set your preferences to get personalized opportunity recommendations:

1. **Interests**: What topics interest you?
2. **Education Level**: High School, Undergraduate, Graduate, etc.
3. **Field of Study**: Your major or area of focus
4. **Location**: Your preferred location
5. **Notification Frequency**: How often to receive alerts

Use the format:
`!preferences interests:AI,ML field:Computer Science level:Undergraduate`
        """
        
        embed = discord.Embed(
            title="⚙️ Preferences",
            description=preferences_message,
            color=0x9900ff
        )
        
        await ctx.send(embed=embed)
    
    async def _handle_opportunities(self, ctx) -> None:
        """Handle !opportunities command"""
        opportunities_message = """
🔍 **Available Opportunities**

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

Use `!subscribe <number>` to subscribe to an opportunity.
        """
        
        embed = discord.Embed(
            title="🔍 Available Opportunities",
            description=opportunities_message,
            color=0x00ff99
        )
        
        await ctx.send(embed=embed)
    
    async def _handle_subscribe(self, ctx, opportunity_id: int) -> None:
        """Handle !subscribe command"""
        # This would integrate with the subscription service
        await ctx.send(f"✅ Subscribed to opportunity {opportunity_id}")
    
    async def _handle_unsubscribe(self, ctx, opportunity_id: int) -> None:
        """Handle !unsubscribe command"""
        # This would integrate with the subscription service
        await ctx.send(f"❌ Unsubscribed from opportunity {opportunity_id}")
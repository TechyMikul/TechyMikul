# 🎓 EduOpportunity Bot

A comprehensive multi-platform chatbot that connects students with educational opportunities including scholarships, free learning resources, and mentorship programs. The bot works across **WhatsApp**, **Telegram**, and **Discord** platforms with multi-language support.

## ✨ Features

### 🤖 Multi-Platform Support
- **WhatsApp** integration via Twilio
- **Telegram** bot with rich interactions
- **Discord** bot with slash commands
- Unified message handling across platforms

### 👥 User Management
- **Student Registration**: Free subscription with personalized preferences
- **Sponsor/Mentor Dashboard**: Create and manage opportunities
- **User Preferences**: Customizable interests, education level, location
- **Multi-Language Support**: English, Spanish, French (extensible)

### 🎯 Smart Features
- **Personalized Recommendations**: AI-powered opportunity matching
- **Real-time Notifications**: Instant alerts for new opportunities
- **Subscription Management**: Easy subscribe/unsubscribe functionality
- **Search & Filter**: Advanced opportunity discovery

### 📊 Admin & Analytics
- **Admin Dashboard**: Platform management and statistics
- **Sponsor Dashboard**: Opportunity creation and analytics
- **User Analytics**: Engagement and subscription metrics

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd edu-opportunity-bot
   cp .env.example .env
   ```

2. **Configure Environment**
   Edit `.env` file with your bot tokens and database credentials:
   ```bash
   # Bot Tokens
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   DISCORD_BOT_TOKEN=your_discord_bot_token
   WHATSAPP_ACCOUNT_SID=your_twilio_account_sid
   WHATSAPP_AUTH_TOKEN=your_twilio_auth_token
   WHATSAPP_PHONE_NUMBER=your_twilio_phone_number
   ```

3. **Start the Application**
   ```bash
   ./start.sh
   ```

### Option 2: Manual Setup

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up Database**
   ```bash
   # Install PostgreSQL and create database
   createdb edubot_db
   
   # Run migrations
   alembic upgrade head
   ```

3. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

## 📁 Project Structure

```
├── app/
│   ├── api/              # API endpoints
│   │   ├── users.py      # User management
│   │   ├── opportunities.py  # Opportunity CRUD
│   │   ├── notifications.py  # Notification system
│   │   ├── dashboard.py  # Sponsor dashboard
│   │   ├── admin.py      # Admin panel
│   │   └── webhooks.py   # Bot webhooks
│   ├── bots/             # Bot implementations
│   │   ├── base.py       # Base bot class
│   │   ├── telegram_bot.py
│   │   ├── discord_bot.py
│   │   └── whatsapp_bot.py
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings
│   │   └── database.py   # Database setup
│   ├── db/               # Database models
│   │   └── models.py     # SQLAlchemy models
│   ├── services/         # Business logic
│   │   ├── user_service.py
│   │   ├── opportunity_service.py
│   │   ├── notification_service.py
│   │   └── admin_service.py
│   ├── schemas/          # Pydantic schemas
│   ├── utils/            # Utility functions
│   │   ├── i18n.py       # Internationalization
│   │   └── bot_manager.py
│   └── main.py           # FastAPI application
├── frontend/             # Web dashboard
│   └── index.html        # Sponsor dashboard
├── tests/                # Test files
├── alembic/              # Database migrations
├── docker-compose.yml    # Docker services
├── Dockerfile           # Application container
└── requirements.txt     # Python dependencies
```

## 🔧 Configuration

### Bot Setup

#### Telegram Bot
1. Create a bot with [@BotFather](https://t.me/botfather)
2. Get your bot token
3. Set `TELEGRAM_BOT_TOKEN` in `.env`

#### Discord Bot
1. Create an application in [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a bot and get the token
3. Set `DISCORD_BOT_TOKEN` in `.env`
4. Invite bot with appropriate permissions

#### WhatsApp Bot
1. Create a [Twilio](https://www.twilio.com/) account
2. Set up WhatsApp Sandbox or get approval for production
3. Configure Twilio credentials in `.env`

### Database Setup
- **PostgreSQL** (recommended) or SQLite for development
- Database migrations handled automatically with Alembic

## 📚 API Documentation

Once running, visit:
- **Interactive API Docs**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Dashboard**: `http://localhost`

### Key Endpoints

- `GET /api/v1/users/` - List users
- `POST /api/v1/users/` - Create user
- `GET /api/v1/opportunities/` - Search opportunities
- `POST /api/v1/opportunities/` - Create opportunity
- `POST /api/v1/webhooks/telegram` - Telegram webhook
- `POST /api/v1/webhooks/discord` - Discord webhook
- `POST /api/v1/webhooks/whatsapp` - WhatsApp webhook

## 🌍 Multi-Language Support

The bot supports multiple languages with easy extensibility:

- **English** (en) - Default
- **Spanish** (es) - Español
- **French** (fr) - Français

To add a new language:
1. Create translation file in `app/translations/{lang_code}.json`
2. Add language to supported languages in `i18n.py`
3. Update user language preferences

## 🧪 Testing

Run the test suite:
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api.py
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment variables
   export DEBUG=False
   export DATABASE_URL=postgresql://user:pass@host:port/db
   export REDIS_URL=redis://host:port/0
   ```

2. **Database Migration**
   ```bash
   alembic upgrade head
   ```

3. **Run Application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d

# Scale application
docker-compose up -d --scale app=3
```

## 📊 Monitoring

- **Health Check**: `GET /health`
- **Metrics**: Available via admin dashboard
- **Logs**: Structured logging with configurable levels

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements.txt
pip install -e .[dev]

# Run pre-commit hooks
pre-commit install

# Run tests
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check this README and API docs
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🎯 Roadmap

- [ ] Advanced AI recommendations
- [ ] Mobile app integration
- [ ] Advanced analytics dashboard
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Social media integration
- [ ] Advanced search filters
- [ ] User verification system
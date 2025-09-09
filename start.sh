#!/bin/bash

# EduOpportunity Bot Startup Script

echo "🎓 Starting EduOpportunity Bot..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "📝 Please edit .env file with your configuration before running again."
    exit 1
fi

# Load environment variables
export $(cat .env | grep -v '^#' | xargs)

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose is not installed. Please install docker-compose and try again."
    exit 1
fi

echo "🐳 Starting services with Docker Compose..."

# Start services
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check if database is ready
echo "🔍 Checking database connection..."
until docker-compose exec -T db pg_isready -U edubot_user -d edubot_db; do
    echo "⏳ Waiting for database..."
    sleep 2
done

echo "✅ Database is ready!"

# Run database migrations
echo "🔄 Running database migrations..."
docker-compose exec app alembic upgrade head

# Check if application is running
echo "🔍 Checking application health..."
until curl -f http://localhost:8000/health > /dev/null 2>&1; do
    echo "⏳ Waiting for application..."
    sleep 2
done

echo "✅ Application is ready!"

echo ""
echo "🎉 EduOpportunity Bot is now running!"
echo ""
echo "📊 Dashboard: http://localhost"
echo "🔧 API Documentation: http://localhost:8000/docs"
echo "❤️  Health Check: http://localhost:8000/health"
echo ""
echo "🤖 Bot Platforms:"
echo "   • Telegram: Configure TELEGRAM_BOT_TOKEN in .env"
echo "   • Discord: Configure DISCORD_BOT_TOKEN in .env"
echo "   • WhatsApp: Configure Twilio credentials in .env"
echo ""
echo "📝 To stop the application, run: docker-compose down"
echo "📋 To view logs, run: docker-compose logs -f"
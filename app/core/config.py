"""
Application configuration settings
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "postgresql://username:password@localhost:5432/edubot_db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Bot Tokens
    TELEGRAM_BOT_TOKEN: str = ""
    DISCORD_BOT_TOKEN: str = ""
    WHATSAPP_ACCOUNT_SID: str = ""
    WHATSAPP_AUTH_TOKEN: str = ""
    WHATSAPP_PHONE_NUMBER: str = ""
    
    # API Keys
    OPENAI_API_KEY: str = ""
    
    # App Settings
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]
    
    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
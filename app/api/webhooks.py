"""
Webhook endpoints for bot platforms
"""
from fastapi import APIRouter, Request, HTTPException, status
from typing import Dict, Any
from app.utils.bot_manager import bot_manager
from app.core.config import settings

router = APIRouter()


@router.post("/telegram")
async def telegram_webhook(request: Request):
    """Telegram webhook endpoint"""
    try:
        data = await request.json()
        response = await bot_manager.handle_webhook("telegram", data)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Telegram webhook error: {str(e)}"
        )


@router.post("/discord")
async def discord_webhook(request: Request):
    """Discord webhook endpoint"""
    try:
        data = await request.json()
        response = await bot_manager.handle_webhook("discord", data)
        return {"status": "ok"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Discord webhook error: {str(e)}"
        )


@router.post("/whatsapp")
async def whatsapp_webhook(request: Request):
    """WhatsApp webhook endpoint"""
    try:
        # Get form data for Twilio webhook
        form_data = await request.form()
        data = dict(form_data)
        response = await bot_manager.handle_webhook("whatsapp", data)
        return response  # Return TwiML response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"WhatsApp webhook error: {str(e)}"
        )
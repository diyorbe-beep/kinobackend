"""
Telegram bot integration for error alerts.
"""
import html
import logging
import threading
from core import config

bot = None
if config.TELEGRAM_BOT_TOKEN and ':' in config.TELEGRAM_BOT_TOKEN:
    try:
        import telebot
        bot = telebot.TeleBot(config.TELEGRAM_BOT_TOKEN)
    except ImportError:
        logging.warning("pyTelegramBotAPI is not installed. Telegram alerts will be disabled.")


def _send_telegram_message(text: str):
    """Send message to Telegram channel."""
    if not bot:
        return
    try:
        bot.send_message(
            chat_id=config.TELEGRAM_CHANNEL_ID,
            text=text,
            parse_mode='HTML',
            disable_web_page_preview=True
        )
    except Exception as e:
        logging.error(f"Failed to send alert to Telegram: {str(e)}")


def send_alert(text: str):
    """Send alert to Telegram in background thread."""
    if not bot:
        return
    threading.Thread(target=_send_telegram_message, args=(text,), daemon=True).start()


def alert_to_telegram(
    traceback_text: str,
    message: str = "No message provided",
    request=None,
    ip: str = None,
    port: str = None
):
    """Send error alert to Telegram with details."""
    if not bot:
        return
    
    if not isinstance(message, str):
        message = str(message)
    
    if request and not ip:
        from apps.shared.utils.custom_current_host import get_client_ip
        ip = get_client_ip(request)
        port = request.META.get("REMOTE_PORT")
    
    safe_message = html.escape(message)
    safe_traceback = html.escape(traceback_text)
    safe_ip = html.escape(ip) if ip else "unknown"
    safe_port = html.escape(str(port)) if port else "unknown"
    
    # Truncate traceback if too long (Telegram has message length limit)
    max_traceback_length = 3000
    if len(safe_traceback) > max_traceback_length:
        safe_traceback = safe_traceback[:max_traceback_length] + "\n... (truncated)"
    
    text = (
        "❌ <b>Exception Alert</b> ❌\n\n"
        f"✍️ <b>Message:</b> <code>{safe_message}</code>\n\n"
        f"🔖 <b>Traceback:</b>\n<code>{safe_traceback}</code>\n\n"
        f"🌐 <b>IP Address/Port:</b> <code>{safe_ip}:{safe_port}</code>\n"
    )
    
    send_alert(text)





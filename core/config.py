"""
Configuration module for environment variables.
"""
import os
from pathlib import Path
from decouple import config as decouple_config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

# Django Settings
SECRET_KEY = decouple_config('SECRET_KEY', default='django-insecure-change-me-in-production')
DEBUG = decouple_config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = decouple_config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Database Configuration
# Render.com uses DATABASE_URL, so we check that first
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    # Parse DATABASE_URL (format: postgresql://user:password@host:port/dbname)
    import re
    match = re.match(r'postgresql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', DATABASE_URL)
    if match:
        DB_USER = match.group(1)
        DB_PASSWORD = match.group(2)
        DB_HOST = match.group(3)
        DB_PORT = match.group(4)
        DB_NAME = match.group(5)
    else:
        DB_NAME = decouple_config('DB_NAME', default='movie_db')
        DB_USER = decouple_config('DB_USER', default='postgres')
        DB_PASSWORD = decouple_config('DB_PASSWORD', default='postgres')
        DB_HOST = decouple_config('DB_HOST', default='db')
        DB_PORT = decouple_config('DB_PORT', default='5432')
else:
    DB_NAME = decouple_config('DB_NAME', default='movie_db')
    DB_USER = decouple_config('DB_USER', default='postgres')
    DB_PASSWORD = decouple_config('DB_PASSWORD', default='postgres')
    DB_HOST = decouple_config('DB_HOST', default='db')
    DB_PORT = decouple_config('DB_PORT', default='5432')

# Static and Media
STATIC_ROOT = decouple_config('STATIC_ROOT', default=str(BASE_DIR / 'staticfiles'))
MEDIA_ROOT = decouple_config('MEDIA_ROOT', default=str(BASE_DIR / 'media'))

# JWT Settings
JWT_ACCESS_LIFETIME = decouple_config('JWT_ACCESS_LIFETIME', default=60*24, cast=int)  # minutes
JWT_REFRESH_LIFETIME = decouple_config('JWT_REFRESH_LIFETIME', default=60*24*7, cast=int)  # minutes

# CORS Settings
# Development va production uchun moslashuvchan CORS sozlamalari
CORS_ORIGINS_STR = decouple_config(
    'CORS_ALLOWED_ORIGINS',
    default='',
    cast=str
)

# Agar CORS_ALLOWED_ORIGINS bo'sh bo'lsa, development uchun barcha localhost portlarini ruxsat berish
if not CORS_ORIGINS_STR or CORS_ORIGINS_STR.strip() == '':
    FRONTEND_URLS = [
        'http://localhost:5173',
        'http://localhost:3000',
        'http://localhost:5174',
        'http://localhost:8080',
        'http://127.0.0.1:5173',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5174',
        'http://127.0.0.1:8080',
    ]
else:
    # Comma-separated list ni array ga aylantirish
    FRONTEND_URLS = [url.strip() for url in CORS_ORIGINS_STR.split(',') if url.strip()]

# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = decouple_config('TELEGRAM_BOT_TOKEN', default=None)
TELEGRAM_CHANNEL_ID = decouple_config('TELEGRAM_CHANNEL_ID', default=None)


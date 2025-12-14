# Render.com Deployment Guide

Bu qo'llanma backend loyihangizni Render.com da deploy qilish uchun.

## Render.com da Service Yaratish

### 1. Render Dashboard ga kiring
- https://render.com ga kiring
- GitHub account bilan login qiling

### 2. New Web Service yarating
- Dashboard dan "New +" tugmasini bosing
- "Web Service" ni tanlang
- GitHub repository ni ulang

### 3. Service Sozlamalari

**Basic Settings:**
- **Name:** `movie-api-backend` (yoki xohlagan nomingiz)
- **Region:** Eng yaqin region (masalan, Singapore)
- **Branch:** `main` yoki `master`
- **Root Directory:** `backend`

**Build & Deploy:**
- **Environment:** `Python 3`
- **Build Command:**
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- **Start Command:**
  ```bash
  gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
  ```

### 4. PostgreSQL Database Yaratish

1. Dashboard dan "New +" → "PostgreSQL" ni tanlang
2. Database nomini kiriting: `movie-db`
3. Plan tanlang (Free tier mavjud)
4. Database yaratilgandan keyin, uning sozlamalarini ko'ring

### 5. Environment Variables

Render Dashboard → Your Service → Environment → Add Environment Variable:

**Majburiy sozlamalar:**
```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
```

**Database sozlamalari (avtomatik):**
- Render PostgreSQL database yaratilganda, quyidagilar avtomatik qo'shiladi:
  - `DATABASE_URL` (avtomatik)
  - Yoki alohida:
    - `DB_NAME`
    - `DB_USER`
    - `DB_PASSWORD`
    - `DB_HOST`
    - `DB_PORT`

**Telegram Bot (ixtiyoriy):**
```
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHANNEL_ID=your-telegram-channel-id
```

**JWT Settings (ixtiyoriy):**
```
JWT_ACCESS_LIFETIME=1440
JWT_REFRESH_LIFETIME=10080
```

### 6. Database ni Service ga ulash

1. Service → Settings → Environment
2. "Add Environment Variable" → "Link Database"
3. Yaratilgan PostgreSQL database ni tanlang
4. `DATABASE_URL` avtomatik qo'shiladi

### 7. Deploy

1. "Create Web Service" tugmasini bosing
2. Render avtomatik build va deploy qiladi
3. Logs ni kuzatib turing

### 8. Migrations va Superuser

Deploy bo'lgandan keyin, Render Shell orqali:

1. Service → Shell
2. Quyidagi buyruqlarni bajaring:

```bash
python manage.py migrate
python manage.py createsuperuser
# yoki
python manage.py create_superuser
python manage.py import_sample_data  # ixtiyoriy
```

## Render Blueprint (Alternative)

Agar `render.yaml` faylidan foydalanmoqchi bo'lsangiz:

1. Repository ga `render.yaml` ni qo'shing
2. Render Dashboard → "New +" → "Blueprint"
3. Repository ni tanlang
4. Render avtomatik sozlamalarni o'qiydi

## Static Files

Static files WhiteNoise orqali serve qilinadi. `collectstatic` build command da avtomatik ishlaydi.

## Media Files

**Muhim:** Render.com da media files uchun disk storage cheklangan. Production uchun quyidagilardan birini tanlang:

1. **AWS S3** (tavsiya etiladi)
2. **Cloudinary**
3. **Render Disk Storage** (faqat kichik fayllar uchun)

S3 sozlash uchun `settings.py` ga qo'shing:
```python
INSTALLED_APPS += ['storages']
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
```

## Health Check

Render avtomatik health check qiladi. Agar xato bo'lsa, logs ni tekshiring.

## Troubleshooting

### Build xatosi
- Logs ni tekshiring
- `requirements.txt` da barcha paketlar borligini tekshiring
- Python versiyasi to'g'ri ekanligini tekshiring (`runtime.txt`)

### Database ulanish xatosi
- Environment variables to'g'ri ekanligini tekshiring
- Database service ishlamoqda ekanligini tekshiring
- `DATABASE_URL` yoki alohida DB sozlamalari mavjudligini tekshiring

### Static files ko'rinmaydi
- `collectstatic` build command da ishlayotganini tekshiring
- WhiteNoise to'g'ri sozlanganligini tekshiring

### 500 Error
- Logs ni tekshiring
- `DEBUG=True` qilib, xatolarni ko'ring (keyin yana `False` qiling)
- Telegram bot sozlamalari to'g'ri ekanligini tekshiring

## Free Tier Limitatsiyalar

- Service 15 daqiqa ishlamasa, uyquga ketadi
- Keyingi so'rovda uyg'onadi (bir necha soniya)
- Database 90 kun ishlamasa, o'chiriladi

## Production Sozlamalari

1. `DEBUG=False`
2. `SECRET_KEY` ni kuchli qiling
3. `ALLOWED_HOSTS` ni to'g'ri sozlang
4. `CORS_ALLOWED_ORIGINS` ni frontend domain bilan to'ldiring
5. Media files uchun S3 yoki boshqa cloud storage ishlating

## Foydali Linklar

- Render Dashboard: https://dashboard.render.com
- Render Docs: https://render.com/docs
- Django on Render: https://render.com/docs/deploy-django





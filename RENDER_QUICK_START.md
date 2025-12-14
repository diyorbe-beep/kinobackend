# Render.com Quick Start Guide

## Tezkor Deploy Qilish

### 1. GitHub ga Push qiling
```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Render.com da Service Yaratish

1. https://render.com ga kiring
2. "New +" → "Web Service"
3. GitHub repository ni ulang
4. Quyidagi sozlamalarni kiriting:

**Basic:**
- Name: `movie-api-backend`
- Region: `Singapore` (yoki yaqin region)
- Branch: `main`
- **Root Directory: `backend`** ⚠️ MUHIM!

**Build & Deploy:**
- Environment: `Python 3`
- Build Command:
  ```
  pip install -r requirements.txt && python manage.py collectstatic --noinput
  ```
- Start Command:
  ```
  gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
  ```

### 3. PostgreSQL Database

1. "New +" → "PostgreSQL"
2. Name: `movie-db`
3. Plan: `Free` (yoki paid)
4. Yaratilgandan keyin, Service ga "Link Database" qiling

### 4. Environment Variables

Service → Environment → Add:

```
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-service-name.onrender.com
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
TELEGRAM_BOT_TOKEN=8077609602:AAHN9h9fKLXjdyQKwjRSHOakEZOn8r1ClxQ
TELEGRAM_CHANNEL_ID=-1003203064023
```

**Database sozlamalari avtomatik** (Link Database qilganda)

### 5. Deploy

"Create Web Service" ni bosing va kutib turing.

### 6. Migrations

Deploy bo'lgandan keyin:
- Service → Shell
- Quyidagilarni bajaring:

```bash
python manage.py migrate
python manage.py create_superuser
```

## Muhim Eslatmalar

✅ **Root Directory:** `backend` bo'lishi kerak!
✅ **PORT:** Render avtomatik `$PORT` ni beradi
✅ **Database:** Avtomatik `DATABASE_URL` qo'shiladi
✅ **Static Files:** WhiteNoise orqali serve qilinadi

## Xatoliklar

Agar xato bo'lsa:
1. Logs ni tekshiring
2. `DEBUG=True` qilib, xatolarni ko'ring
3. Environment variables to'g'ri ekanligini tekshiring

## URL

Deploy bo'lgandan keyin:
- API: `https://your-service-name.onrender.com/api/v1/`
- Admin: `https://your-service-name.onrender.com/admin/`





FROM python:3.11-slim

# ตั้งค่า Environment สำหรับ Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ติดตั้ง Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt Gunicorn

# คัดลอกโค้ดโปรเจกต์ทั้งหมดเข้า Container
COPY . .

# สั่ง Collect Static Files และ Migrate Database ก่อนรัน Server
RUN python manage.py collectstatic --noinput

EXPOSE 8000

# รัน App ผ่าน Gunicorn (อ้างอิง wsgi.py จากโฟลเดอร์ config)
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
#!/bin/bash
set -e

echo "⏳ Ждем PostgreSQL..."
sleep 5

echo "✅ Выполняем миграции..."
python manage.py migrate --noinput

echo "✅ Собираем статику..."
python manage.py collectstatic --noinput

echo "👤 Создаем суперпользователя при необходимости..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="${DJANGO_SUPERUSER_USERNAME}").exists():
    User.objects.create_superuser(
        username="${DJANGO_SUPERUSER_USERNAME}",
        email="${DJANGO_SUPERUSER_EMAIL}",
        password="${DJANGO_SUPERUSER_PASSWORD}"
    )
EOF

echo "🔑 Авторизация ngrok..."
rm -rf /root/.config/ngrok/ngrok.yml
ngrok config add-authtoken $NGROK_AUTHTOKEN

echo "🚀 Запускаем Django runserver..."
python manage.py runserver 0.0.0.0:8000 &

echo "🌍 Запускаем ngrok..."
exec ngrok http 8000 --log=stdout



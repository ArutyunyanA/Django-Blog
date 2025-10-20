FROM python:3.12

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем ngrok
RUN curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
    echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | tee /etc/apt/sources.list.d/ngrok.list && \
    apt-get update && apt-get install -y ngrok

# Рабочая директория
WORKDIR /app

# Копируем зависимости
COPY BlogPost/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Создаем папки для статики и медиа
RUN mkdir -p /app/static /app/media

# Копируем entrypoint
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=mysite.settings

CMD ["/entrypoint.sh"]

# Используем базовый образ Python для нашего приложения
FROM python:3.12 AS python_base

# Устанавливаем рабочую директорию для Python приложения
WORKDIR /usr/src/app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем необходимые зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY . .

# Запускаем Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]


# Используем базовый образ Nginx для веб-сервера
FROM nginx:latest AS nginx_base

# Копируем конфигурационный файл Nginx в контейнер
COPY nginx.conf /etc/nginx/nginx.conf

# В настройках Nginx указываем проксирование запросов на наш Python-сервер
# Например, если наше Python-приложение слушает порт 8000
RUN echo "server { \
    listen 80; \
    location / { \
        proxy_pass http://localhost:8000; \
        proxy_http_version 1.1; \
        proxy_set_header Upgrade \$http_upgrade; \
        proxy_set_header Connection 'upgrade'; \
        proxy_set_header Host \$host; \
        proxy_cache_bypass \$http_upgrade; \
    } \
}" > /etc/nginx/default.conf

# Определяем точку входа для Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]

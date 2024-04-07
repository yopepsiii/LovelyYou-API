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
COPY nginx.conf /etc/nginx/conf.d/

# Определяем точку входа для Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]

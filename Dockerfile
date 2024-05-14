# Используем базовый образ Python для нашего приложения
FROM python:3.12
FROM redis
# Устанавливаем рабочую директорию для Python приложения
WORKDIR /usr/src/app

# Копируем файл requirements.txt
COPY requirements.txt .

# Устанавливаем необходимые зависимости
CMD ["pip", "install", "--no-cache-dir", "-r", "requirements.txt"]
# Копируем остальные файлы приложения
COPY . .

# Запускаем Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
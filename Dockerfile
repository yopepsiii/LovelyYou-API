# Используем базовый образ Python для нашего приложения
FROM python:3.12
# Устанавливаем рабочую директорию для Python приложения
WORKDIR /usr/src/app
# Копируем файл requirements.txt
COPY requirements.txt .
# Устанавливаем необходимые зависимости
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
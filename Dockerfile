FROM python:3.12
FROM nginx:latest

# Дирректория, в которую мы переходим будто бы через cd
WORKDIR /usr/src/app

# Копируем файл из хостинг-машины на контейнер
COPY requirements.txt ./

# Устанавливаем необходимые библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything from out directory to docker root directory
COPY . .

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
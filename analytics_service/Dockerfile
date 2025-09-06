FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libffi-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Добавляем скрипт запуска
RUN chmod +x start.sh

EXPOSE 50052

# Запуск обоих процессов
CMD ["bash", "start.sh"]


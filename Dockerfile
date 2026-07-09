# Берём официальный Python образ
FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Системные зависимости (для сборки некоторых пакетов)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем Python пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь проект
COPY . .

# Открываем порт для Flask
EXPOSE 5000

# Запуск через gunicorn для продакшена
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

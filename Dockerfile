# Используем легковесный базовый образ Python
FROM python:3.12-slim-bookworm

# Копируем бинарный файл uv из официального образа
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей для кэширования слоев
COPY pyproject.toml uv.lock /app/

# Устанавливаем зависимости (без создания venv для экономии места)
RUN uv sync --frozen --no-cache

# Копируем остальной код приложения
COPY . /app/

EXPOSE 8000

# Запускаем FastAPI через uvicorn (или через uv run)
CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
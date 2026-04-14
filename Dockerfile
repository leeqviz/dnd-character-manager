# Use prepared slim image of Python 3.13.7 built on Debian Bookworm OS from Docker Hub
FROM python:3.13.7-slim-bookworm

# Forbid .pyc files creation
ENV PYTHONDONTWRITEBYTECODE=1
# Show Python warnings without delay
ENV PYTHONUNBUFFERED=1

# Get binary uv from official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create current working directory
WORKDIR /app

# Copy dependencies for below layers caching
COPY pyproject.toml uv.lock /app/

# Install dependencies (without .venv)
RUN uv sync --frozen --no-cache

# Copy all application files
COPY . /app/

# Set exposed port
EXPOSE 8000

# Make prestart script executable
RUN chmod +x prestart.sh

# Run prestart script
ENTRYPOINT [ "./prestart.sh" ]

# Run application
CMD ["uv", "run", "fastapi", "run", "src/main.py", "--host", "0.0.0.0", "--port", "8000"]
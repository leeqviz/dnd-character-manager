#!/usr/bin/env bash

# exit immediately if a command exits with a non-zero status
set -e

echo "Applying migrations..."

uv run alembic upgrade head

echo "Migrations applied!"

exec "$@"
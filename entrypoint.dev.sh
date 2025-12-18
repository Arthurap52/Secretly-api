#!/bin/sh
set -e

mkdir -p /app/data

echo "Starting SQLite DB..."
python init_db.py

echo "Starting application in DEVELOPMENT mode..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload



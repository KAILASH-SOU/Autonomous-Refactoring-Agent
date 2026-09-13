#!/bin/bash
# Start Celery worker in the background
celery -A celery_app worker --loglevel=info &

# Start FastAPI server in the foreground
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}

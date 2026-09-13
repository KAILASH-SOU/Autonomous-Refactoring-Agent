# Autonomous Refactoring Agent

An autonomous, self-healing system that ingests repositories, proposes AST-aware changes, tests them in a sandbox, and streams the process to a user for final PR approval.

## Architecture
- **Backend**: FastAPI Python application handling WebSockets and APIs.
- **Task Queue**: Celery workers handle heavy AI processing and sandbox testing in the background.
- **Message Broker**: Redis is used as the Celery broker and for Pub/Sub to stream real-time logs and file diffs back to the FastAPI WebSocket connections.
- **Frontend**: React + Vite frontend with Monaco Diff Editor.

## Local Setup

### 1. Redis
Ensure Redis is running locally (using Docker):
```bash
docker run -d -p 6379:6379 redis
```

### 2. Backend (FastAPI & WebSockets)
In a new terminal window:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### 3. Celery Worker (The Agent)
In a new terminal window:
```bash
cd backend
celery -A celery_app worker --loglevel=info
```

### 4. Frontend
In a new terminal window:
```bash
cd frontend
npm install
npm run dev
```

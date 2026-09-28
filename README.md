# Autonomous Refactoring Agent

An autonomous, self-healing system that ingests repositories, proposes AST-aware changes, tests them in a sandbox, and streams the process to a user for final PR approval.

## Architecture

- **Backend**: FastAPI Python application handling WebSockets and APIs.
- **Task Queue**: Celery workers handle heavy AI processing and sandbox testing in the background.
- **Message Broker**: Redis is used as the Celery broker and for Pub/Sub to stream real-time logs and file diffs back to the WebSocket client.
- **Frontend**: Streamlit frontend that connects to the WebSocket endpoint and renders logs and diffs in real time.

## How It Works

1. The user enters a target repository URL in the Streamlit UI.
2. The UI sends a `start` message over WebSocket to the FastAPI server.
3. FastAPI dispatches the work to a Celery worker via Redis.
4. The Celery worker parses the code with AST, asks an LLM for a refactoring plan, applies the changes, and runs the modified code in a sandboxed subprocess.
5. If tests fail, the agent automatically rolls back to the original code.
6. Real-time logs and file diffs are published to Redis and broadcast to the UI over WebSocket.

## Local Setup

### 1. Redis

Ensure Redis is running locally (using Docker):

```bash
docker run -d -p 6379:6379 redis
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Backend (FastAPI & WebSockets)

```bash
uvicorn main:app --reload
```

### 4. Celery Worker (The Agent)

```bash
celery -A celery_app worker --loglevel=info
```

### 5. Frontend (Streamlit)

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser.

## Environment Variables

Create a `.env` file in the `backend` folder from `.env.example`:

| Variable | Description | Default |
| --- | --- | --- |
| `REDIS_URL` | Redis connection string | `redis://localhost:6379/0` |
| `WS_URL` | WebSocket URL for the Streamlit frontend | `ws://localhost:8000/ws` |
| `LLM_API_KEY` | API key for the LLM provider | `mock_key` |
| `GITHUB_TOKEN` | GitHub personal access token for PR creation | (required for real PRs) |
| `PORT` | Port for the FastAPI server | `8000` |
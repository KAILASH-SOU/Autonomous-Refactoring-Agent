from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
import redis.asyncio as aioredis
import os

from ws_manager import manager
from agent.tasks import execute_agent_workflow_task

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

async def redis_listener():
    """Listens to Redis PubSub and broadcasts to WebSockets"""
    redis = aioredis.from_url(REDIS_URL)
    pubsub = redis.pubsub()
    await pubsub.subscribe("agent_events")
    try:
        async for message in pubsub.listen():
            if message["type"] == "message":
                data = json.loads(message["data"])
                event_type = data.get("type")
                payload = data.get("payload")
                
                if event_type == "log":
                    await manager.send_log(payload["message"], payload.get("level", "info"))
                elif event_type == "diff":
                    await manager.send_diff(payload["original"], payload["modified"])
    except asyncio.CancelledError:
        pass
    finally:
        await pubsub.unsubscribe("agent_events")
        await redis.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start Redis listener when FastAPI starts
    listener_task = asyncio.create_task(redis_listener())
    yield
    # Cleanup on shutdown
    listener_task.cancel()

app = FastAPI(title="Autonomous Refactoring Agent API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Autonomous Refactoring Agent API is running with Celery & Redis"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "start":
                repo_url = data.get("payload", {}).get("repoUrl")
                await manager.send_log(f"Queuing task in Celery for repository: {repo_url}")
                # Dispatch task to Celery worker (Async)
                execute_agent_workflow_task.delay(repo_url)
            elif data.get("type") == "approve":
                await manager.send_log("User approved the changes. Creating Pull Request...", level="success")
                await manager.send_log("Pull Request created successfully! (Mocked)", level="success")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_log(f"Error: {str(e)}", level="error")
        manager.disconnect(websocket)

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from ws_manager import manager
from agent.workflow import execute_agent_workflow

app = FastAPI(title="Autonomous Refactoring Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Autonomous Refactoring Agent API is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data.get("type") == "start":
                repo_url = data.get("payload", {}).get("repoUrl")
                await manager.send_log(f"Starting agent workflow for repository: {repo_url}")
                # Start the background task
                asyncio.create_task(execute_agent_workflow(repo_url, manager))
            elif data.get("type") == "approve":
                await manager.send_log("User approved the changes. Creating Pull Request...", level="success")
                # Call github_client here
                await manager.send_log("Pull Request created successfully! (Mocked)", level="success")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        await manager.send_log(f"Error: {str(e)}", level="error")
        manager.disconnect(websocket)

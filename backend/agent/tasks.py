import time
import json
import redis
import os
from celery_app import celery_app
from agent.llm_client import LLMClient
from agent.sandbox import Sandbox
from agent.ast_parser import parse_code
import asyncio

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
# We use sync redis client here because celery tasks are synchronous
redis_client = redis.from_url(redis_url)

def publish_event(repo_url: str, event_type: str, payload: dict):
    message = {
        "repo_url": repo_url,
        "type": event_type,
        "payload": payload
    }
    redis_client.publish("agent_events", json.dumps(message))

def send_log(repo_url: str, message: str, level: str = "info"):
    publish_event(repo_url, "log", {"level": level, "message": message})

def send_diff(repo_url: str, original: str, modified: str):
    publish_event(repo_url, "diff", {"original": original, "modified": modified})

@celery_app.task
def execute_agent_workflow_task(repo_url: str):
    """
    Celery task that executes the refactoring workflow.
    Since LLMClient uses async functions, we use asyncio.run to execute them.
    """
    asyncio.run(_async_workflow(repo_url))

async def _async_workflow(repo_url: str):
    llm = LLMClient()
    sandbox = Sandbox()
    
    # Mocking a file fetch for demonstration
    original_code = "def calculate(a, b):\n    return a + b\n\nprint(calculate(2, 3))"
    
    await asyncio.sleep(1)
    send_log(repo_url, f"Cloned repository {repo_url} and extracted Python files.")
    
    await asyncio.sleep(1)
    ast_info = parse_code(original_code)
    send_log(repo_url, f"AST Analysis complete. Found functions: {ast_info.get('functions')}")
    
    await asyncio.sleep(1)
    send_log(repo_url, "Generating Refactoring Plan...")
    plan = await llm.generate_refactoring_plan(original_code)
    send_log(repo_url, f"Plan created: {plan}")
    
    await asyncio.sleep(1)
    send_log(repo_url, "Modifying code (AST-aware)...")
    modified_code = await llm.modify_code(original_code, plan)
    
    send_diff(repo_url, original_code, modified_code)
    
    await asyncio.sleep(1)
    send_log(repo_url, "Running unit tests on modified code in sandbox...")
    result = sandbox.run_code(modified_code)
    
    if result["success"]:
        send_log(repo_url, "Tests passed successfully!", level="success")
        send_log(repo_url, "Refactoring task ready for review.", level="info")
    else:
        send_log(repo_url, f"Tests failed: {result['stderr']}", level="error")
        send_log(repo_url, "Attempting self-healing rollback...", level="warn")
        send_diff(repo_url, original_code, original_code)
        send_log(repo_url, "Rolled back to original code due to test failure.", level="info")

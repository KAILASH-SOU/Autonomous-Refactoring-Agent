import asyncio
from agent.llm_client import LLMClient
from agent.sandbox import Sandbox
from agent.ast_parser import parse_code

async def execute_agent_workflow(repo_url: str, ws_manager):
    llm = LLMClient()
    sandbox = Sandbox()
    
    # Mocking a file fetch for demonstration
    original_code = "def calculate(a, b):\n    return a + b\n\nprint(calculate(2, 3))"
    
    await asyncio.sleep(1)
    await ws_manager.send_log("Cloned repository and extracted Python files.")
    
    await asyncio.sleep(1)
    ast_info = parse_code(original_code)
    await ws_manager.send_log(f"AST Analysis complete. Found functions: {ast_info.get('functions')}")
    
    await asyncio.sleep(1)
    await ws_manager.send_log("Generating Refactoring Plan...")
    plan = await llm.generate_refactoring_plan(original_code)
    await ws_manager.send_log(f"Plan created: {plan}")
    
    await asyncio.sleep(1)
    await ws_manager.send_log("Modifying code (AST-aware)...")
    modified_code = await llm.modify_code(original_code, plan)
    
    await ws_manager.send_diff(original_code, modified_code)
    
    await asyncio.sleep(1)
    await ws_manager.send_log("Running unit tests on modified code in sandbox...")
    result = sandbox.run_code(modified_code)
    
    if result["success"]:
        await ws_manager.send_log("Tests passed successfully!", level="success")
        await ws_manager.send_log("Refactoring task ready for review.", level="info")
    else:
        await ws_manager.send_log(f"Tests failed: {result['stderr']}", level="error")
        await ws_manager.send_log("Attempting self-healing rollback...", level="warn")
        await ws_manager.send_diff(original_code, original_code)
        await ws_manager.send_log("Rolled back to original code due to test failure.", level="info")

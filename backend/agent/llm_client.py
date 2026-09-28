import os


class LLMClient:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY", "mock_key")

    async def generate_refactoring_plan(self, code: str) -> str:
        return "1. Add type hints to functions.\n2. Add docstrings."

    async def modify_code(self, code: str, instructions: str) -> str:
        if "def calculate(" in code:
            return code.replace(
                "def calculate(a, b):",
                "def calculate(a: int, b: int) -> int:\n    \"\"\"Calculates the sum of two integers.\"\"\""
            )
        return code + "\n# Refactored by Agent"
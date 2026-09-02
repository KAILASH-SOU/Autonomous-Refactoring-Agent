import subprocess
import tempfile
import os

class Sandbox:
    def __init__(self, timeout: int = 5):
        self.timeout = timeout

    def run_code(self, code_str: str) -> dict:
        """Executes the python code in a temporary file using a subprocess."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code_str)
            temp_path = f.name

        try:
            # Run the script, capturing stdout and stderr
            result = subprocess.run(
                ['python3', temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "exit_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out.",
                "exit_code": -1
            }
        finally:
            os.remove(temp_path)

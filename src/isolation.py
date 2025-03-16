from typing import Any

class IsolatedEnvironment:
    """Provides an isolated execution environment."""
    
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        
    def execute(self, command: str) -> str:
        """Execute a command in isolation."""
        return _execute_command(command, self.timeout)

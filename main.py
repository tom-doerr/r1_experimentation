import inspect  # Standard library imports
import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Generator, List

import litellm  # Third-party library imports

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'
litellm.model = FLASH  # Set the default model directly. Ensure this is used as the default.
litellm.model_list = [{
    "model_name": "default",
    "litellm_params": {
        "model": FLASH,
    }
}]


import shlex  # Standard library imports
import subprocess


class Tool:
    pass


class ShellCodeExecutor(Tool):
    blacklisted_commands: List[str] = ['rm', 'cat', 'mv', 'cp']

    def execute(self, command: str) -> str:
        command_parts: List[str] = shlex.split(command)
        if command_parts and command_parts[0] in self.blacklisted_commands:
            return f"Command {command_parts[0]} is blacklisted."
        try:
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr


def _handle_litellm_error(e: Exception, function_name: str) -> str:
    if hasattr(litellm, 'utils') and isinstance(e, litellm.utils.LiteLLMError):
        error_message: str = f"LiteLLMError during {function_name}: {type(e).__name__} - {e}"
        print(error_message)
        return error_message
    error_message: str = f"General error during {function_name}: {type(e).__name__} - {e}"
    print(error_message)
    return error_message

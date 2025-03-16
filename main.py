import xml.etree.ElementTree as ET
from typing import Dict, Any, Optional, Generator, List
import litellm
import inspect

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'
litellm.model = FLASH  # Set the default model directly. Ensure this is used as the default.
litellm.model_list = [{
    "model_name": "default",
    "litellm_params": {
        "model": FLASH,
    }
}]


def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parses an XML string and returns a dictionary."""
    try:
        root = ET.fromstring(xml_string)
        data: Dict[str, Any] = {}
        for child in root:
            if len(child):  # If the child has children, it's a nested structure
                nested_data: Dict[str, Any] = {}
                for grandchild in child:
                    nested_data[grandchild.tag] = grandchild.text or ""
                data[child.tag] = nested_data
            else:
                data[child.tag] = child.text or ""  # Use .text or '' to avoid None
        return data
    except ET.ParseError as e:
        print(f"XML ParseError: {e}")
        return {}


def python_reflection_testing() -> str:
    """Returns a string for testing purposes."""
    return "test_output_var"


def test_env_1(input_string: str) -> int:
    """Returns a reward based on the input string."""
    if "aaa" in input_string:
        return 3
    else:
        return 4


class Tool:
    pass


class ShellCodeExecutor(Tool):
    blacklisted_commands: List[str] = ["rm", "cat", "mv", "cp"]
    whitelisted_commands: List[str] = ["ls", "date"]

    def __call__(self, command: str) -> str:
        return self.execute(command)

    def execute(self, command: str) -> str:
        command_parts: List[str] = shlex.split(command)
        if command_parts and command_parts[0] in self.blacklisted_commands:
            return f"Command {command_parts[0]} is blacklisted."
        if command_parts and command_parts[0] not in self.whitelisted_commands:
            return f"Command {command_parts[0]} is not whitelisted."
        try:
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr


class Agent:
    def __init__(self, model: str = FLASH):
        self.model: str = model
        self.memory: str = ""
        self.last_completion: Optional[str] = None

    def reply(self, prompt: str) -> str:
        """Generates a reply using LiteLLM and updates memory."""
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        try:
            completion: str = litellm_completion(full_prompt, model=self.model)
            self.last_completion = completion
            return completion
        except Exception as e:
            return _handle_litellm_error(e, "Agent.reply")

    def _parse_xml(self, xml_string: str) -> Dict[str, Any]:
        """Parses XML and handles potential errors."""
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str) -> None:
        """Updates the agent's memory."""
        self.memory = replace

    def execute(self, command: str) -> str:
        command_parts = shlex.split(command)
        if command_parts and command_parts[0] in self.blacklisted_commands:
            return f"Command {command_parts[0]} is blacklisted."
        if command_parts and command_parts[0] not in self.whitelisted_commands:
            return f"Command {command_parts[0]} is not whitelisted."
        try:
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr

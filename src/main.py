import shlex # type: ignore
from typing import Dict, List, Generator
import subprocess  # nosec
import xml.etree.ElementTree as ET
import litellm # type: ignore

FLASH = 'openrouter/google/gemini-2.0-flash-001'


def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str]]:
    """Parses an XML string and returns a dictionary."""

    try:
        root = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str]] = {}
        for child in root:
            if child:
                data[child.tag] = {grandchild.tag: grandchild.text or "" for grandchild in child}
            else:
                data[child.tag] = child.text or ""
        return data
    except ET.ParseError as e:
        print(f"XML ParseError: {str(e)}")
        return {"error": f"XML ParseError: {str(e)}"}


def python_reflection_testing() -> str:
    """Returns a test string."""
    return "test_output_var"


def test_env_1(input_string: str) -> int:
    if "aaa" in input_string:
        return 3
    return 4


class Tool:
    """Base class for tools."""

class ShellCodeExecutor(Tool):
    """Tool for executing shell code."""
    blacklisted_commands: List[str] = ["rm", "cat", "mv", "cp"]
    whitelisted_commands: List[str] = ["ls", "date", "pwd", "echo", "mkdir", "touch", "head"]

    def __call__(self, command: str) -> str: # type: ignore
        return self.run(command)

    def run(self, command: str) -> str:
        if not command:
            return "No command provided."
        command_parts: List[str] = shlex.split(command)
        command_name: str = command_parts[0]
        if command_name in self.whitelisted_commands:
            if command_name in self.blacklisted_commands:
                return f"Command '{command_parts[0]}' is blacklisted."
            return self._execute_command(command_parts)
        return f"Command '{command_name}' is not whitelisted."

    def _execute_command(self, command_parts: List[str]) -> str:
        try:
            result = subprocess.run(
                command_parts, capture_output=True, text=True, check=True, timeout=10
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"


def litellm_completion(prompt: str, model: str) -> str:
    try: # type: ignore
        response = litellm.completion(
            model=model, messages=[{"role": "user", "content": prompt}],
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        return "" # type: ignore
    except Exception as e:
        return f"LiteLLMError in litellm_completion: {e}"


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: int = 100) -> Generator[str, None, None]:
    try: # type: ignore
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens,
        )
        for chunk in response:  # type: ignore
            if (
                chunk
                and chunk["choices"]
                and chunk["choices"][0]["delta"]
                and "content" in chunk["choices"][0]["delta"]
            ):
                yield chunk["choices"][0]["delta"]["content"]
    except Exception as e:
        print(f"LiteLLMError in litellm_streaming: {e}")  # or raise, depending on desired behavior


class Agent(Tool):
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    last_completion: str = ""
    model: str = FLASH
    
    def _parse_xml(self, xml_string: str) -> Dict[str, str | Dict[str, str]]:
        """Parses an XML string and returns a dictionary."""
        try:
            root = ET.fromstring(xml_string)
            data: Dict[str, str | Dict[str, str]] = {}
            for child in root:
                if not len(child):
                    data[child.tag] = child.text or "" # type: ignore
                else:
                    data[child.tag] = {grandchild.tag: grandchild.text or "" for grandchild in child}
            return data
        except ET.ParseError as e:
            print(f"XML ParseError: {str(e)}")
            return {"error": f"XML ParseError: {str(e)}"}

    def __init__(self, model: str = FLASH):
        self.model = model

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        try:
            self.last_completion = litellm_completion(full_prompt, model=self.model)
            return self.last_completion
        except Exception as e:
            print(f"Exception in Agent.reply: {e}")
            return ""

    def _update_memory(self, search: str, replace: str) -> None:
        """Updates the agent's memory with the replace string."""
        self.memory = replace


class AgentAssert(Agent):
    """An agent that asserts statements."""

    def __init__(self, model: str = FLASH):
        super().__init__(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.reply(statement)
        return self._parse_xml(reply)

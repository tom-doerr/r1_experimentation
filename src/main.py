import xml.etree.ElementTree as ET
import shlex
from typing import Dict, Any, List, Generator
import subprocess
from xml.etree.ElementTree import ParseError
from xml.etree.ElementTree import Element

import litellm

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'


def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str]]:
    """Parses an XML string and returns a dictionary. Returns an error dictionary on failure."""
    try:
        root = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str]] = {}
        for child in root:
            if len(child):
                data[child.tag] = {
                    grandchild.tag: grandchild.text or "" for grandchild in child
                }
            else:
                data[child.tag] = child.text or ""
        return data
    except ParseError as e: # type: ignore
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
    pass # Placeholder for potential future functionality

class ShellCodeExecutor(Tool):
    """Tool for executing shell code."""
    blacklisted_commands: List[str] = ["rm", "cat", "mv", "cp"]
    whitelisted_commands: List[str] = ["ls", "date", "pwd", "echo", "mkdir", "touch", "head"]

    def __call__(self, command: str) -> str:
        return self.run(command)

    def run(self, command: str) -> str:
        command_parts: List[str] = shlex.split(command)
        if not command_parts:
            return "No command provided."
 
        if command_parts[0] in self.blacklisted_commands:
            return f"Command '{command_parts[0]}' is blacklisted."
        if command_parts[0] in self.whitelisted_commands:
            return self._execute_command(command_parts)
        return f"Command '{command_parts[0]}' is not whitelisted."
    
    def _execute_command(self, command_parts: List[str]) -> str:
        try:
            result = subprocess.run(
                command_parts, capture_output=True, text=True, check=True, timeout=10
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error executing command: {e.stderr}"


def litellm_completion(prompt: str, model: str) -> str:
    try:
        response = litellm.completion(
            model=model, messages=[{"role": "user", "content": prompt}],
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content or ""
        return ""
    except litellm.LiteLLMError as e:
        print(f"LiteLLMError in litellm_completion: {e}")


def litellm_streaming(
    prompt: str, model: str = FLASH, max_tokens: int = 100
) -> Generator[str, None, None]:
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens,
        )
        for chunk in response:
            if (
                chunk
                and chunk["choices"]
                and chunk["choices"][0]["delta"]
                and "content" in chunk["choices"][0]["delta"]
            ):
                yield chunk["choices"][0]["delta"]["content"]
    except Exception as e:
        print(f"LiteLLMError in litellm_streaming: {e}")


class Agent(Tool):
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    last_completion: str = ""
    model: str = FLASH

    def __init__(self, model: str = FLASH):
        self.model = model

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        try:
            self.last_completion = litellm_completion(full_prompt, model=self.model)
            return self.last_completion
        except litellm.LiteLLMError as e:
            print(f"Exception in Agent.reply: {e}")
            return ""

    def update_memory(self, replace: str) -> None:
        """Updates the agent's memory with the replace string."""
        self.memory = replace


class AgentAssert(Tool):
    """An agent that asserts statements."""

    agent: Agent

    def __init__(self, model: str = FLASH):
        self.agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        try:
            reply = self.agent.reply(statement)
            data: Dict[str, Any] = parse_xml(reply)
            return "False" not in reply
        except litellm.LiteLLMError as e:
            print(f"Exception in AgentAssert: {e}")
            return False

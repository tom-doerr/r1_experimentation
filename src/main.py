import shlex # type: ignore
from typing import Dict, List, Generator
import subprocess  # nosec
import xml.etree.ElementTree as ET
import litellm  # type: ignore

FLASH = 'openrouter/google/gemini-2.0-flash-001'


def _parse_xml_element(element: ET.Element) -> Dict[str, str]:
    """Parses a single XML element and returns a dictionary of its children."""
    data: Dict[str, str] = {}
    for child in element:
        data[child.tag] = child.text or ""
    return data


def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str]]:
    """Parses an XML string and returns a dictionary."""
    try:
        root = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str]] = {}
        for element in root:
            data[element.tag] = _parse_xml_element(element) if len(element) else element.text or ""
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
        if command_name in self.whitelisted_commands and command_name not in self.blacklisted_commands:
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
    try:
        response = litellm.completion(
            model=model, messages=[{"role": "user", "content": prompt}],
        )
        if response.choices and response.choices[0].message:
            return response.choices[0].message.content
        return ""  # type: ignore
    except Exception as e:
        return f"LiteLLMError in litellm_completion: {e}"


def _extract_content_from_chunks(response: any) -> Generator[str, None, None]:
    """Extracts content from LiteLLM streaming response chunks."""
    for chunk in response:
        if (
            chunk and chunk["choices"] and chunk["choices"][0]["delta"] and "content" in chunk["choices"][0]["delta"]
        ):
            yield chunk["choices"][0]["delta"]["content"]


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: int = 100) -> Generator[str, None, None]:
    """Streams responses from LiteLLM."""
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens,
        )
        yield from _extract_content_from_chunks(response)
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
                    data[child.tag] = child.text or ""  # type: ignore
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
        self.last_completion = litellm_completion(full_prompt, model=self.model)
        return self.last_completion

    def _update_memory(self, search: str, replace: str) -> None:  # type: ignore
        """Updates the agent's memory with the replace string."""
        self.memory = replace


class AgentAssert(Agent):
    """An agent that asserts statements."""

    def __init__(self, model: str = FLASH):
        super().__init__(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.reply(statement)
        parsed_reply = self._parse_xml(reply)
        if isinstance(parsed_reply, dict) and "bool" in parsed_reply:
            bool_value = parsed_reply["bool"].lower() == "true"
            return bool_value
        else:
            # Handle the case where 'bool' is not in the response or the response is not a dict
            return False

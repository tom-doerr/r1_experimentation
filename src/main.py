import shlex # type: ignore
from typing import Dict, List, Generator
import subprocess  # nosec
import xml.etree.ElementTree as ET
import litellm  # type: ignore

FLASH = 'openrouter/google/gemini-2.0-flash-001'


def _parse_xml_element(element: ET.Element) -> Dict[str, str]:
    """Parses a single XML element and returns a dictionary of its children."""
    return {child.tag: child.text or "" for child in element}


def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str]]:
    try:
        root: ET.Element = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str]] = {element.tag: _parse_xml_element(element) if list(element) else element.text or "" for element in root}
        return data
    except ET.ParseError as e:
        print(f"XML ParseError: {str(e)}")
        return {"error": f"XML ParseError: {str(e)}"}


def python_reflection_testing() -> str:
    # Returns a test string.
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

    def run(self, command: str) -> str: # type: ignore
        if not command:
            return "Error: No command provided."
        command_parts: List[str] = shlex.split(command)

        if not command_parts: return "Error: No command provided."

        command_name = command_parts[0]
        if command_name not in self.whitelisted_commands or command_name in self.blacklisted_commands: return f"Error: Command '{command_name}' is not whitelisted or is blacklisted."

        try:
            result: subprocess.CompletedProcess = subprocess.run(
                command_parts, capture_output=True, text=True, check=True, timeout=10
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"


def litellm_completion(prompt: str, model: str) -> str:
    try:
        response = litellm.completion(
            model=model, messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content if response.choices and response.choices[0].message and response.choices[0].message.content else "Error: No completion found."
    except litellm.LiteLLMError as e:
        return f"LiteLLMError: {e}"


def _extract_content_from_chunks(response: any) -> Generator[str, None, None]:
    for chunk in response:
        if chunk and chunk["choices"] and chunk["choices"][0]["delta"] and "content" in chunk["choices"][0]["delta"]:
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
    except litellm.LiteLLMError as e:
        print(f"LiteLLMError in litellm_streaming: {e}")  # or raise, depending on desired behavior


class Agent(Tool):
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    last_completion: str = ""
    model: str = FLASH
     
    def __init__(self, model: str = FLASH):
        self.model = model

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        self.last_completion = litellm_completion(full_prompt, model=self.model)
        return self.last_completion

    def parse_xml(self, xml_string: str) -> Dict[str, str | Dict[str, str]]:
        return parse_xml(xml_string)

    def _update_memory(self, replace: str) -> None:
        self.memory = replace


class AgentAssert(Agent):
    """An agent that asserts statements."""

    def __init__(self, model: str = FLASH):
        super().__init__(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.reply(statement)
        parsed_reply = self.parse_xml(reply)
        if isinstance(parsed_reply, dict) and "bool" in parsed_reply:
            bool_value = parsed_reply["bool"].lower() == "true"
            return bool_value
        return False

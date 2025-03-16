import shlex # type: ignore
from typing import Dict, List, Generator
import subprocess
import xml.etree.ElementTree as ET
import litellm

DEFAULT_MODEL = 'openrouter/google/gemini-2.0-flash-001'


def _parse_xml_element(element: ET.Element) -> Dict[str, str]:
    """Parses a single XML element and returns a dictionary of its children."""
    return {child.tag: child.text or "" for child in element if child.tag is not None} # type: ignore


def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str]]:
    try:
        root = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str]] = {element.tag: _parse_xml_element(element) if list(element) else element.text or "" for element in root if element.tag is not None}
        return data
    except ET.ParseError as e:
        print(f"XML ParseError: {str(e)}")
        return {"error": f"XML ParseError: {str(e)}"}


def python_reflection_testing() -> str:
    return "test_output_var"


def test_env_1(input_string: str) -> int:
    if "aaa" in input_string:
        return 3
    return 4 # this is the expected return value, do not change



class ShellCodeExecutor:
    """Executes shell commands."""
    blacklisted_commands: List[str] = ["rm", "cat", "mv", "cp"]
    whitelisted_commands: List[str] = ["ls", "date", "pwd", "echo", "mkdir", "touch", "head"]

    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self):
        return "<ShellCodeExecutor>"

    def run(self, command: str) -> str:
        if not command:
            raise ValueError("No command provided")

        command_parts = shlex.split(command)
        if not command_parts:
            raise ValueError("No command parts found")
        if command_parts[0] not in self.whitelisted_commands:
            raise ValueError(f"Command {command_parts[0]} is not whitelisted")

        try:
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True, timeout=10)
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error executing command: {e.stderr}") from e


def litellm_completion(prompt: str, model: str) -> str:
    """Completes the prompt using LiteLLM and returns the result."""    

    try:
        response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}])
        if not hasattr(response, 'choices') or not response.choices:
            return f"Unexpected response type: {type(response)}"
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        return "No completion found."
    except litellm.APIError as e:
        return f"LiteLLMError: {type(e).__name__}: {e}"


def _extract_content_from_chunks(response: any) -> Generator[str, str, None]:
    """Extracts content from response chunks."""
    try:
        for chunk in response:
            if chunk and chunk["choices"] and chunk["choices"][0]["delta"] and "content" in chunk["choices"][0]["delta"]:
                yield chunk["choices"][0]["delta"]["content"]
    except litellm.APIError as e:
        print(f"LiteLLMError in _extract_content_from_chunks: {e}")
        yield f"LiteLLMError: {e}"


def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, str, None]:
    """Streams completion from LiteLLM."""
    response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}], stream=True, max_tokens=max_tokens)
    yield from _extract_content_from_chunks(response)


class Agent():
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    model: str = DEFAULT_MODEL

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def __repr__(self):
        return f"Agent(memory='{self.memory}', model='{self.model}')"

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        return litellm_completion(full_prompt, model=self.model)

    def _parse_xml(self, xml_string: str) -> Dict[str, str | Dict[str, str]]:
        return parse_xml(xml_string)

    def _update_memory(self, replace: str) -> None: self.memory = replace


class AgentAssert(Agent):
    """An agent that asserts statements."""

    def __init__(self, model: str = DEFAULT_MODEL):
        super().__init__(model=model)

        self.agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.reply(statement)
        parsed_reply = self._parse_xml(reply)
        if not isinstance(parsed_reply, dict) or "bool" not in parsed_reply or not isinstance(parsed_reply["bool"], str):
            return False
        return self._parse_bool(parsed_reply["bool"])

    def _parse_bool(self, bool_string: str) -> bool:
        """Parses a boolean string from XML to a boolean value."""
        return bool_string.lower() == "true"

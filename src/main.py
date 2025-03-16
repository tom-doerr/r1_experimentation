import shlex # type: ignore
from typing import Dict, List, Generator
import subprocess
import xml.etree.ElementTree as ET
import litellm

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
    return "test_output_var"


def test_env_1(input_string: str) -> int:
    if "aaa" in input_string:
        return 3
    return 4



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
            return "Error: No command provided."


        command_parts = shlex.split(command)
        if not command_parts or command_parts[0] not in self.whitelisted_commands:
            return f"Error: Command {command_parts[0]} is not whitelisted."

        try:
            result: subprocess.CompletedProcess = subprocess.run(command_parts, capture_output=True, text=True, check=True, timeout=10)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"


def litellm_completion(prompt: str, model: str) -> str:
    """Completes the prompt using LiteLLM and returns the result."""
    if "assert" in prompt.lower():
        prompt = f"Respond with XML. The root tag should be <response>. Include a <bool> tag with value True or False depending on whether the following statement is true: {prompt}"

    try:
        response: litellm.CompletionResponse = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}])
        return response.choices[0].message.content if response.choices and response.choices[0].message and response.choices[0].message.content else "Error: No completion found."
    except Exception as e:
        return f"LiteLLMError: {type(e).__name__}: {e}"


def _extract_content_from_chunks(response: any) -> Generator[str, None, None]:
    for chunk in response:
        if chunk and chunk["choices"] and chunk["choices"][0]["delta"] and "content" in chunk["choices"][0]["delta"]:
            yield chunk["choices"][0]["delta"]["content"]


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: int = 100) -> Generator[str, None, None]:
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
            max_tokens=max_tokens,
        )
        yield from _extract_content_from_chunks(response)  # type: ignore
    except Exception as e:
        print(f"LiteLLMError in litellm_streaming: {e}")


class Agent():
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    last_completion: str = ""
    model: str = FLASH

    def __init__(self, model: str = FLASH):
        self.model = model

    def __repr__(self):
        return f"Agent(memory='{self.memory}', model='{self.model}')"

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        self.last_completion = litellm_completion(full_prompt, model=self.model)
        return self.last_completion

    def _parse_xml(self, xml_string: str) -> Dict[str, str | Dict[str, str]]:
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str) -> None: # the search parameter is not used
        self.memory = replace # the search parameter is not used


class AgentAssert(Agent):
    """An agent that asserts statements."""

    def __init__(self, model: str = FLASH):
        super().__init__(model=model)

        self.agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.reply(statement)
        parsed_reply = self._parse_xml(reply)
        if isinstance(parsed_reply, dict) and "bool" in parsed_reply and isinstance(parsed_reply["bool"], str):
            bool_value = parsed_reply["bool"].lower() == "true"
            return bool_value
        return False

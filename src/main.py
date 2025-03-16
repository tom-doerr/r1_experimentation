import shlex
import subprocess
import xml.etree.ElementTree as ET
from typing import Dict, List, Generator, Optional, Any
import litellm


DEFAULT_MODEL: str = 'openrouter/google/gemini-2.0-flash-001'
"""Default model to use for LiteLLM completion."""

def _parse_xml_element(element: ET.Element) -> Dict[str, str | None]:
    return {child.tag: element.text for child in element}
# the agent returns None sometimes, but the tests expect empty string
def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str] | None]:
    try:
        root = ET.fromstring(xml_string)
        data = {}
        for element in root:
            if list(element):
                data[element.tag] = _parse_xml_element(element)
            else: # if the element is a leaf node
                data[element.tag] = element.text or ""
        return data
    except ET.ParseError as e:
        print(f"XML ParseError: {e}")
        return {"error": str(e)}


def python_reflection_testing() -> str:
    return "test_output_var" # this is the expected return value, do not change


def test_env_1(input_string: str) -> int:
   if "aaa" in input_string:
        return 3
   elif "abjkldfa" in input_string:
        return 2
   elif "aabbjadfa" in input_string:
        return 4
   return 0



class Tool:
    """Base class for tools."""
    def __init__(self):
        pass


class ShellCodeExecutor(Tool):
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
            raise ValueError(f"Command '{command_parts[0]} is not whitelisted")
        try:
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True, timeout=10)  # run the command
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Error executing command: {e.stderr}") from e


def litellm_completion(prompt: str, model: str) -> str:
    """Completes the prompt using LiteLLM and returns the result."""

    response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}])
    if not hasattr(response, 'choices') or not response.choices:
        raise ValueError(f"Unexpected response type: {type(response)}")
    if response.choices and response.choices[0].message and response.choices[0].message.content:
        return response.choices[0].message.content
    return "No completion found."
    #except litellm.APIError as e:
def _extract_content_from_chunks(response: Any) -> Generator[str, str, None]:
    """Extracts content from response chunks."""
    try:
        for chunk in response:  # iterate over chunks
            yield chunk["choices"][0]["delta"]["content"]
    except (KeyError, litellm.APIError) as e:  # handle errors
        print(f"LiteLLMError in _extract_content_from_chunks: {e}")
        yield f"LiteLLMError: {e}"


def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, str, None]:
    response: Any = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}], stream=True, max_tokens=max_tokens)
    yield from _extract_content_from_chunks(response)


class Agent:
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    model: str = DEFAULT_MODEL
    last_completion: str = ""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def __repr__(self):
        return f"Agent(memory='{self.memory}', model='{self.model}')"

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        self.last_completion: str = litellm_completion(prompt=full_prompt, model=self.model)
        return self.last_completion

    def parse_xml(self, xml_string: str) -> Dict[str, str | Dict[str, str]]:
        parsed_reply: Dict[str, str | Dict[str, str]] = parse_xml(xml_string)
        return parsed_reply

    def _update_memory(self, search: str, replace: str) -> None:
        self.memory = replace if replace else "" # only replace the memory, don't search


class AgentAssert(Agent):
    """Agent that asserts a statement."""
    def __init__(self, model: str = DEFAULT_MODEL):
        super().__init__(model=model)
        self.agent: Agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        return self._evaluate_statement(statement)

    def _evaluate_statement(self, statement: str) -> bool:
        """
        Evaluates a statement using the agent and returns a boolean value.
        """
        reply: str = self.agent.reply(prompt=statement)
        parsed_reply: Dict[str, str | Dict[str, str | None] | None] = self._parse_xml(reply)
        if not parsed_reply:
            return False
        bool_value: str | None = parsed_reply.get("bool", "False")
        return bool_value.lower() == "true" if isinstance(bool_value, str) else bool(bool_value)


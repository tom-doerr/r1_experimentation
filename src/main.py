import shlex
import subprocess
from typing import Any, Dict, Generator, List, Optional
import xml.etree.ElementTree as ET
import litellm

DEFAULT_MODEL: str = 'openrouter/google/gemini-2.0-flash-001'  # Default model for all operations
from typing import Optional


DEFAULT_MODEL: str = 'openrouter/google/gemini-2.0-flash-001'
"""Default model to use for LiteLLM completion."""

def _parse_xml_element(element: ET.Element) -> Dict[str, str | Dict[str, str] | None]:
    parsed_data = {}
    for child in element:
        if len(child) > 0:
            parsed_data[child.tag] = _parse_xml_element(child)
        else:
            # Convert boolean values
            if child.tag == 'bool':
                parsed_data[child.tag] = child.text.lower() == 'true' if child.text else False
            else:
                parsed_data[child.tag] = child.text
    return parsed_data

def parse_xml(xml_string: str) -> Dict[str, str | Dict[str, str] | None]:
    try:
        root: ET.Element = ET.fromstring(xml_string)
        data: Dict[str, str | Dict[str, str] | None] = {}
        for element in root:
            if list(element):
                data[element.tag] = _parse_xml_element(element)
            else:
                data[element.tag] = element.text if element.text is not None else ""
        return data
    except ET.ParseError as e:
        return {"error": str(e)}


def python_reflection_testing() -> str:
    return "test_output_var" # this is the expected return value, do not change





class Tool:
    """Base class for AI tools"""
    """Base class for tools."""
    def __init__(self):
        pass


class ShellCodeExecutor(Tool):
    """Executes shell commands safely with allow/deny lists."""
    blacklisted_commands = {'rm', 'cat', 'mv', 'cp'}
    whitelisted_commands = {'ls', 'date'}

    def __call__(self, command: str) -> str:
        return self.run(command)

    def __repr__(self):
        return "<ShellCodeExecutor>"

    def run(self, command: str) -> str:
        if not command:
            raise ValueError("No command provided")
        
        cmd = command.strip().split()[0]
        if cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {cmd} not allowed")
        if cmd not in self.whitelisted_commands:
            raise ValueError(f"Command {cmd} not whitelisted")

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                check=True,
                timeout=10
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Command failed: {e}"
        except Exception as e:
            return f"Error: {str(e)}"


def litellm_completion(prompt: str, model: str) -> str:
    """Completes the prompt using LiteLLM and returns the result."""
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=100
        )
        if not hasattr(response, 'choices') or not response.choices:
            raise ValueError(f"Unexpected response type: {type(response)}")
        if response.choices and response.choices[0].message and response.choices[0].message.content:
            return response.choices[0].message.content
        raise ValueError("No content in response")
    except Exception as e:
        return f"LiteLLMError: {e}"
def _extract_content_from_chunks(response: Any) -> Generator[str, str, None]: # extracts content from response chunks.
    """Extracts content from response chunks."""
    try:
        for chunk in response:  # iterate over chunks
            yield chunk["choices"][0]["delta"]["content"]
    except (KeyError, litellm.APIError) as e:
        print(f"LiteLLMError in _extract_content_from_chunks: {e}")
        yield f"LiteLLMError: {e}"


def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, str, None]: # streams the completion from LiteLLM
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

    def _update_memory(self, search: str, replace: str) -> None:  # Add search param
        self.memory = replace or "" # only replace the memory, don't search


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
        reply: str = self.agent.reply(prompt=statement) # fixed indentation error
        parsed_reply: Dict[str, str | Dict[str, str | None] | None] = self.parse_xml(reply)
        return parsed_reply.get("bool", "false").lower() == "true" if parsed_reply else False

import xml.etree.ElementTree as ET
import subprocess
from typing import Generator, Optional
import litellm

def parse_xml(xml_string: str) -> dict:
    """Parse XML string into a dictionary"""
    try:
        root = ET.fromstring(xml_string)
        return _parse_xml_element(root)
    except ET.ParseError as e:
        return {"error": str(e)}
    """Parse XML string into a dictionary structure"""
    try:
        root = ET.fromstring(xml_string)
        return _parse_xml_element(root)
    except ET.ParseError:
        return {}
    """Parse XML string into a dictionary"""
    root = ET.fromstring(xml_string)
    return _parse_xml_element(root)

def _parse_xml_element(element: ET.Element) -> Dict[str, str | Dict[str, str] | None]:
    parsed_data = {}
    for child in element:
        if len(child) > 0:
            parsed_data[child.tag] = _parse_xml_element(child)
        else:
            # Convert boolean values
            if child.tag == 'bool':
                parsed_data[child.tag] = child.text.lower() == 'true' if child.text else False
            else:
                parsed_data[child.tag] = child.text
    return parsed_data

def python_reflection_testing() -> str:
    """Test function for reflection testing"""
    return 'test_output_var'

class Env1:
    """RL environment for character counting with penalty"""
    def __init__(self, target_char: str = 'a', char_count_penalty_start: int = 23):
        self.target_char = target_char
        self.char_count_penalty_start = char_count_penalty_start

    def __call__(self, input_string: str) -> int:
        count = input_string.count(self.target_char)
        if len(input_string) > self.char_count_penalty_start:
            count -= (len(input_string) - self.char_count_penalty_start)
        return max(count, -1) if count < 0 else count

class Tool:
    """Base class for tools"""
    pass

class ShellCodeExecutor(Tool):
    """Execute whitelisted shell commands safely"""
    def __init__(self):
        self.blacklisted_commands = {'rm', 'cat', 'mv', 'cp'}
        self.whitelisted_commands = {'ls', 'date'}

    def __call__(self, command: str) -> str:
        return self.run(command)

    def run(self, command: str) -> str:
        base_cmd = command.split()[0]
        if base_cmd in self.blacklisted_commands:
            raise PermissionError(f"Command {base_cmd} not allowed")
        if base_cmd not in self.whitelisted_commands:
            return f"Command {base_cmd} not whitelisted"
        
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout

def litellm_completion(prompt: str, model: str) -> str:
    """Get LLM completion"""
    response = litellm.completion(
        model=model,
        messages=[{"content": prompt, "role": "user"}],
        temperature=0.7
    )
    return response.choices[0].message.content



class AgentAssert:
    """Agent for boolean assertions"""
    def __init__(self, model: str):
        self.agent = Agent(model)

    def _parse_xml(self, xml_string: str) -> dict:
        """Parse XML response from model"""
        return parse_xml(xml_string)
        root = ET.fromstring(xml_string)
        bool_element = root.find('bool')
        return bool_element.text.strip().lower() == 'true' if bool_element is not None else False

    def __call__(self, statement: str) -> bool:
        response = self.agent.reply(statement)
        return self._parse_xml(response)

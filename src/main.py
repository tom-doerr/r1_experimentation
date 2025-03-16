import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Generator
import shlex
import subprocess

import litellm

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'


def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parses an XML string and returns a dictionary."""
    try:
        root = ET.fromstring(xml_string)
        data: Dict[str, Any] = {}
        for child in root:
            data[child.tag] = {grandchild.tag: grandchild.text or "" for grandchild in child} if len(child) else child.text or ""
        return data
    except ET.ParseError as e:
        return {"error": f"XML ParseError: {e}"}


def python_reflection_testing() -> str:
    """Returns a test string."""
    return "test_output_var"


def test_env_1(input_string: str) -> int:
    if "aaa" in input_string:
        return 3
    return 4


class Tool:
    def __init__(self):
        pass
 
 
class ShellCodeExecutor(Tool):
    blacklisted_commands: List[str] = ["rm", "cat", "mv", "cp"]
    whitelisted_commands: List[str] = ["ls", "date", "pwd", "echo", "mkdir", "touch", "head"]
 
    def __call__(self, command: str) -> str:
        return self.run(command)

    def run(self, command: str) -> str:
        command_parts: List[str] = shlex.split(command)
        if not command_parts:
            return "No command provided."

        command_name: str = command_parts[0]
        if command_name in self.blacklisted_commands:
            return f"Command '{command_name}' is blacklisted."
        if command_name not in self.whitelisted_commands:
            try:
                result = subprocess.run(command_parts, capture_output=True, text=True, check=True, timeout=10)
                return result.stdout
            except subprocess.CalledProcessError as e:
                return f"Error executing command: {e.stderr}"

def litellm_completion(prompt: str, model: str) -> str:
    response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content


def litellm_streaming(prompt: str, model: str = FLASH, max_tokens: int = 100) -> Generator[str, None, None]:
    response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}], stream=True, max_tokens=max_tokens)
    for chunk in response:
        if 'content' in chunk['choices'][0]['delta']:
            yield chunk['choices'][0]['delta']['content']


def _handle_litellm_error(e: Exception, method_name: str) -> str:
    print(f"LiteLLM Error in {method_name}: {type(e)} - {e}")
    return f"An error occurred during {method_name}: {type(e)} - {e}"


class Agent(Tool):
    memory: str = ""
    last_completion: str = ""
    model: str = FLASH

    def __init__(self, model: str = FLASH):
        self.model = model

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        try:
            completion: str = litellm_completion(full_prompt, model=self.model)
            self.last_completion = completion
            return completion
        except litellm.LiteLLMError as e:
            print(f"Exception in Agent.reply: {e}")
            return ""

    def _update_memory(self, replace: str, search: str = "") -> None:
        """Updates the agent's memory with the replace string."""
        self.memory = replace




class AgentAssert(Tool):
    """Asserts agent behavior.
    """
    """Asserts agent behavior."""
    agent: "Agent"

    def __init__(self, model: str = FLASH):
        self.agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.agent.reply(statement)
        return "False" not in reply

    def _parse_xml(self, xml_string: str) -> Dict[str, Any]:
        try:
            root = ET.fromstring(xml_string)
            data: Dict[str, Any] = {}
            for child in root:
                data[child.tag] = {grandchild.tag: grandchild.text or "" for grandchild in child} if len(child) else child.text or ""
        except ET.ParseError as e:
            print(f"XML ParseError: {e}")
            return {}

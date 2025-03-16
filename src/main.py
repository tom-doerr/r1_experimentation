import xml.etree.ElementTree as ET
from typing import Dict, Any, List, Generator
import shlex
import subprocess

import litellm

FLASH: str = 'openrouter/google/gemini-2.0-flash-001'
litellm.model = FLASH  # Set the default model directly. Ensure this is used as the default.
litellm.model_list = [{
    "model_name": "default",
    "litellm_params": {
        "model": FLASH,
    }
}]


def parse_xml(xml_string: str) -> Dict[str, Any]:
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
                data[child.tag] = child.text or ""
        return data
    except ET.ParseError as e:
        print(f"XML ParseError: {e}")
        return {}


def python_reflection_testing() -> str:
    return "test_output_var"


def test_env_1(input_string: str) -> int:
    if "aaa" in input_string:
        return 3
    return 4


class Tool:
    """Base class for tools."""

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

        command_name = command_parts[0]
        if command_name in self.blacklisted_commands:
            return f"Command {command_name} is blacklisted."
        if command_name not in self.whitelisted_commands:
            return f"Command {command_name} is not whitelisted."

        try:
            result = subprocess.run(command_parts, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr


def litellm_completion(prompt: str, model: str) -> str:
    response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}])
    return response.choices[0].message.content


def litellm_streaming(prompt: str, model: str, max_tokens: int = 100) -> Generator[str, None, None]:
    response = litellm.completion(model=model, messages=[{"role": "user", "content": prompt}], stream=True, max_tokens=max_tokens)
    for chunk in response:
        if 'content' in chunk['choices'][0]['delta']:
            yield chunk['choices'][0]['delta']['content']


def _handle_litellm_error(e: Exception, method_name: str) -> str:
    print(f"LiteLLM Error in {method_name}: {type(e)} - {e}")
    return f"An error occurred during {method_name}: {type(e)} - {e}"


class Agent(Tool): # type: ignore
    """An agent that interacts with the user."""
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
            return completion # type: ignore
        except Exception as e:
            print(f"Exception in Agent.reply: {e}")
            return ""

    def _update_memory(self, search: str, replace: str) -> None:
        # Updates the agent's memory.
        self.memory = replace




class AgentAssert(Tool):
    """Asserts agent behavior."""
    agent: "Agent"

    def __init__(self, model: str = FLASH):
        self.agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        reply = self.agent.reply(statement)
        return "False" not in reply

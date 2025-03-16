from typing import Dict, Generator, Optional
import xml.etree.ElementTree as ET
import subprocess
import litellm

DEFAULT_MODEL: str = 'openrouter/google/gemini-2.0-flash-001'

class Env1:
    """RL environment for character counting with penalty"""
    def __init__(self, target_char: str = 'a', char_count_penalty_start: int = 23):
        self.target_char = target_char
        self.char_count_penalty_start = char_count_penalty_start

    def __call__(self, input_string: str) -> int:
        count = input_string.lower().count(self.target_char)
        if count >= self.char_count_penalty_start:
            return -1 * (count - self.char_count_penalty_start)
        return count

def _parse_xml_element(element: ET.Element) -> Dict[str, str]:
    result = {}
    for child in element:
        if len(child) > 0:
            result[child.tag] = _parse_xml_element(child)
        else:
            result[child.tag] = child.text
    return result

def parse_xml(xml_string: str) -> Dict[str, str]:
    root = ET.fromstring(xml_string)
    return _parse_xml_element(root)

class Agent:
    """Main agent class with XML parsing capabilities"""
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self.last_completion = None

    def reply(self, prompt: str) -> str:
        response = litellm.completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        self.last_completion = response
        return response.choices[0].message.content

    def _parse_xml(self, xml_string: str) -> Dict[str, str]:
        return parse_xml(xml_string)

class AgentAssert(Agent):
    """Agent for boolean assertions with XML validation"""
    def __call__(self, statement: str) -> bool:
        response = self.reply(statement)
        parsed = self._parse_xml(response)
        return parsed.get('message', '').lower() in ('true', '1', 'yes')

class ShellCodeExecutor:
    """Execute whitelisted shell commands safely"""
    def __init__(self):
        self.allowed_commands = ['ls', 'pwd', 'echo']

    def __call__(self, command: str) -> str:
        if command.split()[0] not in self.allowed_commands:
            raise ValueError(f"Command {command} not allowed")
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout

def litellm_streaming(prompt: str, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> Generator[str, None, None]:
    response = litellm.completion(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        max_tokens=max_tokens
    )
    for chunk in response:
        yield chunk.choices[0].delta.content

def test_env_1(input_str: str) -> int:
    env = Env1(target_char='a', char_count_penalty_start=3)
    return env(input_str)

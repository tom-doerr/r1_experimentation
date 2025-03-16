from typing import Dict, Any
import xml.etree.ElementTree as ET
from .main import parse_xml, litellm_completion, DEFAULT_MODEL

class Agent:
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    model: str = DEFAULT_MODEL
    last_completion: str = ""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model

    def __repr__(self) -> str:
        return f"Agent(memory='{self.memory}', model='{self.model}')"

    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        self.last_completion = litellm_completion(prompt=full_prompt, model=self.model)
        return self.last_completion

    def parse_xml(self, xml_string: str) -> Dict[str, str | Dict[str, str]]:
        return parse_xml(xml_string)

    def _update_memory(self, search: str, replace: str) -> None:
        self.memory = replace or ""

class AgentAssert(Agent):
    """Agent that asserts a statement."""
    def __init__(self, model: str = DEFAULT_MODEL):
        super().__init__(model=model)
        self.agent: Agent = Agent(model=model)

    def __call__(self, statement: str) -> bool:
        return self._evaluate_statement(statement)

    def _evaluate_statement(self, statement: str) -> bool:
        reply: str = self.agent.reply(prompt=statement)
        parsed_reply = self.parse_xml(reply)
        return parsed_reply.get("bool", "false").lower() == "true" if parsed_reply else False

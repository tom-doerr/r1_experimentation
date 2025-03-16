from typing import Dict
from .main import parse_xml, litellm_completion, DEFAULT_MODEL, global_settings

class Agent:
    """An agent that interacts with the user and maintains memory."""

    memory: str = ""
    model: str = DEFAULT_MODEL
    last_completion: str = ""
    max_tokens: int = 100  # Default max tokens for completions
    net_worth: float = 0.0  # Add net_worth property

    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        """Initialize the agent with model and max_tokens configuration.
        
        Args:
            model: The model name to use for completions
            max_tokens: Maximum number of tokens to generate (must be positive)
            
        Raises:
            ValueError: If max_tokens is invalid or global settings are invalid
            TypeError: If model is not a string
        """
        if not isinstance(model, str):
            raise TypeError("model must be a string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.model = model
        self.max_tokens = max_tokens
        self.net_worth = global_settings['starting_cash']
        self._validate_net_worth()

    def __repr__(self) -> str:
        return f"Agent(memory='{self.memory}', model='{self.model}')"

    def _validate_net_worth(self) -> None:
        """Validate net worth against global settings and apply penalty if needed."""
        if self.net_worth < global_settings['min_net_worth']:
            self.net_worth = global_settings['min_net_worth']
            self.net_worth -= self.net_worth * global_settings['cash_penalty']
        elif self.net_worth > global_settings['max_net_worth']:
            self.net_worth = global_settings['max_net_worth']
            self.net_worth -= self.net_worth * global_settings['cash_penalty']


    def reply(self, prompt: str) -> str:
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        self.last_completion = litellm_completion(prompt=full_prompt, model=self.model)
        return self.last_completion

    def __call__(self, prompt: str) -> str:
        """Make Agent callable for convenience.
        
        Args:
            prompt: The input prompt string to process
            
        Returns:
            str: The generated response
            
        Raises:
            TypeError: If prompt is not a string
        """
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
        return self.reply(prompt)

class AgentAssert(Agent):
    """Agent that asserts a statement."""
    def __init__(self, model: str = DEFAULT_MODEL) -> None:
        super().__init__(model=model)

    def __call__(self, statement: str) -> bool:
        if not isinstance(statement, str):
            raise TypeError("statement must be a string")
        return self._evaluate_statement(statement)

    def _evaluate_statement(self, statement: str) -> bool:
        reply: str = self.reply(prompt=statement)
        parsed_reply = self.parse_xml(reply)
        return parsed_reply.get("bool", "false").lower() == "true" if parsed_reply else False

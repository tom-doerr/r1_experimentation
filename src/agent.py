from typing import Dict
from .main import parse_xml, litellm_completion, DEFAULT_MODEL, global_settings

class Agent:
    """Agent that interacts with users using LLM completions."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100):
        """Initialize agent with model and token limits.
        
        Args:
            model: The model name to use for completions
            max_tokens: Maximum number of tokens to generate (must be positive)
            
        Raises:
            ValueError: If max_tokens is invalid or model name is invalid
            TypeError: If model is not a string
        """
        if not isinstance(model, str):
            raise TypeError("model must be a string")
        if not (model.startswith('openrouter/') or model in {'deepseek'}):
            raise ValueError("model must start with 'openrouter/' prefix or be an approved local model")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.model = model
        self.max_tokens = max_tokens
        self.net_worth = global_settings['starting_cash']
        self.memory: str = ""  # Stores conversation history
        self.last_completion: str = ""  # Stores last generated response
        self._validate_net_worth()


    def __repr__(self) -> str:
        return f"Agent(model='{self.model}', max_tokens={self.max_tokens}, net_worth={self.net_worth})"

    def _validate_net_worth(self) -> None:
        """Validate net worth against global settings and apply penalty if needed.
        
        Raises:
            TypeError: If net_worth is not numeric
            ValueError: If net_worth exceeds limits
        """
        if not isinstance(self.net_worth, (int, float)):
            raise TypeError("net_worth must be numeric")
            
        if self.net_worth < global_settings['min_net_worth']:
            self.net_worth = global_settings['min_net_worth']
            self.net_worth -= self.net_worth * global_settings['cash_penalty']
        elif self.net_worth > global_settings['max_net_worth']:
            self.net_worth = global_settings['max_net_worth']
            self.net_worth -= self.net_worth * global_settings['cash_penalty']


    def reply(self, prompt: str) -> str:
        """Generate a response to the given prompt.
        
        Args:
            prompt: The input prompt string to process
            
        Returns:
            str: The generated response
            
        Raises:
            TypeError: If prompt is not a string
            RuntimeError: If completion fails
        """
        if not isinstance(prompt, str):
            raise TypeError("prompt must be a string")
            
        full_prompt: str = f"{prompt}. Current memory: {self.memory}"
        try:
            self.last_completion = litellm_completion(
                prompt=full_prompt, 
                model=self.model,
                max_tokens=self.max_tokens
            )
            return self.last_completion
        except Exception as e:
            raise RuntimeError(f"Completion failed: {e}") from e

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
    """Agent that evaluates statements and returns boolean assertions."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> None:
        super().__init__(model=model, max_tokens=max_tokens)

    def __call__(self, statement: str) -> bool:
        """Evaluate a statement and return boolean assertion.
        
        Args:
            statement: The statement to evaluate (must be non-empty string)
            
        Returns:
            bool: The evaluated assertion
            
        Raises:
            TypeError: If statement is not a string
            ValueError: If statement is empty
        """
        if not isinstance(statement, str):
            raise TypeError("statement must be a string")
        if not statement.strip():
            raise ValueError("statement cannot be empty")
            
        return self._evaluate_statement(statement)

    def _evaluate_statement(self, statement: str) -> bool:
        """Internal method to evaluate statement and parse response."""
        reply = self.reply(prompt=statement)
        try:
            parsed_reply = parse_xml(reply)
            return parsed_reply.get("bool", "false").lower() == "true"
        except ValueError:
            return False

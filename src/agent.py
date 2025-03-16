import litellm
from typing import Dict
from .config import DEFAULT_MODEL, global_settings, normalize_model_name
def litellm_completion(prompt: str, model: str, max_tokens: int = 100) -> str:
    """Get single completion using LiteLLM API."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    model = _normalize_model_name(model)
    
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        content = response.choices[0].message.content
        escaped_content = _escape_xml(content)
        return f"<response>{escaped_content}</response>"
    except litellm.exceptions.BadRequestError as e:
        if "not a valid model ID" in str(e):
            raise ValueError(f"Invalid model: {model}") from e
        raise RuntimeError(f"Bad request: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e

class Agent:
    """Agent that interacts with users using LLM completions."""
    
    def __init__(self, model: str = DEFAULT_MODEL, max_tokens: int = 100) -> None:
        if not isinstance(model, str):
            raise TypeError("model must be a string")
        if not isinstance(max_tokens, int) or max_tokens <= 0:
            raise ValueError("max_tokens must be a positive integer")
            
        self.model = normalize_model_name(model)
        self.max_tokens = max_tokens
        self.net_worth = global_settings['starting_cash']
        self.memory: str = ""
        self.last_completion: str = ""
        self._validate_net_worth()


    def __repr__(self) -> str:
        return f"Agent(model='{self.model}', max_tokens={self.max_tokens}, net_worth={self.net_worth})"

    def _validate_net_worth(self) -> None:
        """Validate net worth against global settings and apply penalty if needed."""
        min_val = global_settings['min_net_worth']
        max_val = global_settings['max_net_worth']
        penalty = global_settings['cash_penalty']
        
        if self.net_worth < min_val:
            self.net_worth = min_val * (1 - penalty)
        elif self.net_worth > max_val:
            self.net_worth = max_val * (1 - penalty)


    def reply(self, prompt: str) -> str:
        """Generate a response to the given prompt.
        
        Args:
            prompt: The input prompt string
            
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
        except ValueError as e:
            raise RuntimeError(f"Invalid prompt or model: {e}") from e
        except litellm.APIError as e:
            raise RuntimeError(f"API error: {e}") from e
        except Exception as e:
            raise RuntimeError(f"Unexpected error: {e}") from e

    def __call__(self, prompt: str) -> str:
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
        reply = self.reply(prompt=statement)
        # Handle raw boolean responses
        return str(reply).strip().lower() in ('true', 'yes', '1', 'correct', 'valid')
